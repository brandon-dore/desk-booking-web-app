from typing import Union
from urllib.parse import urlencode
from fastapi import Depends, FastAPI, HTTPException, status, Response, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import datetime

from app import crud, security, schemas, auth, models
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal

# Inital FastAPI Setup

app = FastAPI(title="Desk Booking API", swagger_ui_parameters={
              "operationsSorter": "method"},
              version=1.0, root_path="/")

# Allowing for CORS, so frontend can call on API endpoints

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for retriving database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
def flatten_query_string_lists(request: Request, call_next):
    '''
    Middleware to convert query strings into the correct format for fastAPI.
    Correctly formatted strings will be unaffected.
    Example input: http://localhost:8000/users?&range=[0,9]&sort=["id","ASC"]
    Converted to : http://localhost:8000/users?&range=0&range=9&sort=id&sort=ASC

    Parameters:
            request (Request): 
            call_next (function): 
            
    Returns:
        callback_func (function or None): 
    '''

    flattened = []

    for key, value in request.query_params.multi_items():
        value = value.strip("[]")
        for entry in value.split(','):
            entry = entry.strip('""')
            if entry.isdigit():
                flattened.append((key, int(entry)))
            else:
                flattened.append((key, entry))

    request.scope["query_string"] = urlencode(
        flattened, doseq=True).encode("utf-8")

    return call_next(request)

# Start of request mapping, majority of functions only perform a call to crud.py with some error handling
# More complex functions are commented on. All crud.py functions are commented to help with understanding here.

# Redirect to swagger documentation when accessing the "/" route

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')


# User Endpoints


@app.post("/login", response_model=schemas.Token)
def login_and_get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''
    Checks if a user exists using the authenticate user function. If they don't they are unautherised.
    If they do exist a JWT is generated using authentication functions and returned.

    Parameters:
            db (Session): A session of a database (from dependancy)
            form_data (OAuth2PasswordRequestForm): Contains data for registering a user

    Returns:
        JWT (dictionary): A dictionary containing the JWTs access and refresh token as well as the token type
    '''
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.timedelta(
        minutes=security.REFRESH_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": auth.generic_token_creation(data={"sub": user.username}, expires_delta=access_token_expires, token_type="access"),
        "refresh_token": auth.generic_token_creation(data={"sub": user.username}, expires_delta=refresh_token_expires, token_type="refresh"),
        "token_type": "bearer"
    }

# Registers both endpoints to keep to REST standards


@app.post("/register", response_model=schemas.User)
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=list[schemas.User])
def read_users(response: Response, range: Union[list[int], None] = Query(default=None), sort: Union[list[str], None] = Query(default=['id', 'ASC']), db: Session = Depends(get_db)):
    users = crud.get_all_entities(db, range=range, sort=sort, model=models.User)
    response.headers["Content-Range"] = str(len(users))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_entity(db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/me/", response_model=schemas.User)
def read_own_details(current_user: schemas.User = Depends(auth.get_current_active_user)):
    return current_user


@app.patch("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    existing_user = crud.get_entity(db, id=user_id, model=models.User)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud.update_entity(db=db, entity_to_update=existing_user, updates=user, model=models.User)
    return updated_user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_to_delete = crud.get_entity(db, id=user_id, model=models.User)
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_entity(db, id=user_id, model=models.User)

# Room Endpoints


@app.post("/rooms", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_name(db, room_name=room.name)
    if db_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    return crud.create_room(db=db, room=room)


@app.get("/rooms", response_model=list[schemas.Room])
def read_rooms(response: Response, range: Union[list[int], None] = Query(default=None), sort: Union[list[str], None] = Query(default=['id', 'ASC']), db: Session = Depends(get_db)):
    rooms = crud.get_all_entities(db, range=range, sort=sort, model=models.Room)
    response.headers["Content-Range"] = str(len(rooms))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return rooms


@app.get("/rooms/{room_id}", response_model=schemas.Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_entity(db, id=room_id, model=models.Room)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@app.patch("/rooms/{room_id}")
def update_room(room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    existing_room = crud.get_entity(db, id=room_id, model=models.Room)
    if existing_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    updated_room = crud.update_entity(db=db, entity_to_update=existing_room, updates=room, model=models.Room)
    return updated_room


@app.delete("/rooms/{room_id}", status_code=204)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_to_delete = crud.get_entity(db, id=room_id, model=models.Room)
    if room_to_delete is None:
        raise HTTPException(status_code=404, detail="Room not found")
    crud.delete_entity(db, id=room_id, model=models.Room)


# Desk Endpoints


@app.post("/desks", response_model=schemas.Desk)
def create_desk(desk: schemas.DeskCreate, db: Session = Depends(get_db)):
    db_desk = crud.get_desk_by_room_and_number(
        db, room_id=desk.room_id, desk_number=desk.number)
    if db_desk:
        raise HTTPException(status_code=400, detail="Desk already exists")
    return crud.create_desk(db=db, desk=desk)


@app.get("/desks", response_model=list[schemas.Desk])
def read_desks(response: Response, range: Union[list[int], None] = Query(default=None), sort: Union[list[str], None] = Query(default=None), db: Session = Depends(get_db)):
    desks = crud.get_all_entities(db, range=range, sort=sort, model=models.Desk)
    response.headers["Content-Range"] = str(len(desks))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return desks


@app.get("/rooms/{room_id}/desks", response_model=list[schemas.Desk])
def read_desks_in_room(response: Response, room_id: int, range: Union[list[int], None] = Query(default=None), sort: Union[list[str], None] = Query(default=['id', 'ASC']), db: Session = Depends(get_db)):
    desks = crud.get_desks_in_room(
        db, room_id=room_id, range=range, sort=sort)
    response.headers["Content-Range"] = str(len(desks))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    if desks is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return desks


@app.get("/desks/{desk_id}", response_model=schemas.Desk)
def read_desk(desk_id: int, db: Session = Depends(get_db)):
    db_desk = crud.get_entity(db, id=desk_id, model=models.Desk)
    if db_desk is None:
        raise HTTPException(status_code=404, detail="Desk not found")
    return db_desk


@app.patch("/desks/{desk_id}")
def update_desk(desk_id: int, desk: schemas.DeskUpdate, db: Session = Depends(get_db)):
    existing_desk = crud.get_entity(db, id=desk_id, model=models.Desk)
    if existing_desk is None:
        raise HTTPException(status_code=404, detail="Desk not found")
    updated_desk = crud.update_entity(db=db, entity_to_update=existing_desk, updates=desk, model=models.Desk)
    return updated_desk


@app.delete("/desks/{desk_id}", status_code=204)
def delete_desk(desk_id: int, db: Session = Depends(get_db)):
    desk_to_delete = crud.get_entity(db, id=desk_id, model=models.Desk)
    if desk_to_delete is None:
        raise HTTPException(status_code=404, detail="Desk not found")
    crud.delete_entity(db, id=desk_id, model=models.Desk)


# Booking Endpoints


@app.post("/bookings", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = crud.get_booking_by_desk_and_date(
        db, desk_id=booking.desk_id, date=booking.date)
    if db_booking:
        raise HTTPException(status_code=400, detail="Booking already exists")
    return crud.create_booking(db=db, booking=booking)


@app.get("/bookings", response_model=list[schemas.Booking])
def read_bookings(response: Response, range: Union[list[int], None] = Query(default=None), sort: Union[list[str], None] = Query(default=['id', 'ASC']), db: Session = Depends(get_db)):
    bookings = crud.get_all_entities(db, range=range, sort=sort, model=models.Booking)
    response.headers["Content-Range"] = str(len(bookings))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    return bookings


@app.get("/bookings/{booking_id}", response_model=schemas.Booking)
def read_bookings(booking_id: int, response: Response, db: Session = Depends(get_db)):
    db_booking = crud.get_entity(db, id=booking_id, model=models.Booking)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


@app.get("/rooms/{room_id}/bookings/{date}", response_model=list[schemas.Booking])
def read_bookings_by_room(response: Response, date: datetime.date, room_id: int, range: Union[list[int], None] = Query(default=None), sort: Union[list[str], None] = Query(default=['id', 'ASC']), db: Session = Depends(get_db)):
    db_booking = crud.get_bookings_by_room(db, date=date, room_id=room_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


@app.patch("/bookings/{booking_id}")
def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)):
    existing_booking = crud.get_entity(db, id=booking_id, model=models.Booking)
    if existing_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    updated_booking = crud.update_entity(db=db, entity_to_update=existing_booking, updates=booking, model=models.Booking)
    return updated_booking


@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_to_delete = crud.get_entity(db, id=booking_id, model=models.Booking)
    if booking_to_delete is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    crud.delete_entity(db, id=booking_id, model=models.Booking)


@app.get("/users/me/bookings/", response_model=list[schemas.BookingSummary])
async def read_own_items(current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(get_db)):
    return crud.get_users_bookings(db=db, user_id=current_user.id)

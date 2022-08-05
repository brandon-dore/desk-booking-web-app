from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Tuple, Union

import datetime
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Desk Booking API")

# Check if Database is a month (or week) old an delete if so?


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_email}", response_model=schemas.User)
def read_user(user_email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Teams

@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_name(db, team_name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    return crud.create_team(db=db, team=team)


@app.get("/teams/", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams


@app.get("/teams/{team_name}", response_model=schemas.Team)
def read_team(team_name: str, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_name(db, team_name=team_name)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

# Rooms

@app.post("/rooms/", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_name(db, room_name=room.name)
    if db_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    return crud.create_room(db=db, room=room)


@app.get("/rooms/", response_model=list[schemas.Room])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms


@app.get("/rooms/{room_name}", response_model=schemas.Room)
def read_room(room_name: str, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_name(db, room_name=room_name)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

# Desks

@app.post("/desks/", response_model=schemas.Desk)
def create_desk(desk: schemas.DeskCreate, db: Session = Depends(get_db)):
    db_user = crud.get_desk_by_room_and_number(
        db, room_name=desk.room, desk_number=desk.number)
    if db_user:
        raise HTTPException(status_code=400, detail="Desk already exists")
    return crud.create_desk(db=db, desk=desk)


@app.get("/desks/", response_model=list[schemas.Desk])
def read_desks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_desks(db, skip=skip, limit=limit)
    return users


@app.get("/desks/{room_name}/{desk_number}", response_model=schemas.Desk)
def read_desk(room_name: str, desk_number: int, db: Session = Depends(get_db)):
    db_user = crud.get_desk_by_room_and_number(
        db, room_name=room_name, desk_number=desk_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Desk not found")
    return db_user

# Bookings

@app.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = crud.get_booking_by_desk_and_date(
        db, desk_number=booking.desk_number, room_name=booking.room_name, date=booking.date)
    if db_booking:
        raise HTTPException(status_code=400, detail="Booking already exists")
    return crud.create_booking(db=db, booking=booking)


@app.get("/bookings/", response_model=list[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db=db, skip=skip, limit=limit)
    print(bookings[0].desk)
    return bookings



@app.get("/bookings/{date}/{user_email}", response_model=schemas.Booking)
def read_booking(date: datetime.date, user_email: str, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(
        db, date=date, user_email=user_email)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

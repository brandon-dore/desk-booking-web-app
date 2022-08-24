from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

import datetime

from api import models, schemas, auth

from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, _start: int = 0, _end: int = 100, _order: str = "ASC", _sort: str = "id"):
    users_id = getattr(models.User, _sort).asc() if _order.upper(
    ) == "ASC" else getattr(models.User, _sort).desc()
    return db.query(models.User).order_by(users_id).offset(_start).limit(_end).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=auth.get_hashed_password(user.password), admin=user.admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User, updates: schemas.UserUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    updated_user = get_user(db, user.id)
    return updated_user


def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()


def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def get_room_by_name(db: Session, room_name: str):
    return db.query(models.Room).filter(models.Room.name == room_name).first()


def get_rooms(db: Session, _start: int = 0, _end: int = 100, _order: str = "ASC", _sort: str = "id"):
    rooms_id = getattr(models.Room, _sort).asc() if _order.upper(
    ) == "ASC" else getattr(models.Room, _sort).desc()
    return db.query(models.Room).order_by(rooms_id).offset(_start).limit(_end).all()


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room: models.Room, updates: schemas.RoomUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)
    db.commit()
    updated_room = get_user(db, room.id)
    return updated_room


def delete_room(db: Session, room_id: int):
    db.query(models.Room).filter(models.Room.id == room_id).delete()
    db.commit()


def get_desk(db: Session, desk_id: int):
    return db.query(models.Desk).filter(models.Desk.id == desk_id).first()


def get_desk_by_room_and_number(db: Session, desk_number: int, room_id: int):
    return db.query(models.Desk).filter(and_(models.Desk.room_id == room_id, models.Desk.number == desk_number)).first()


def get_desks(db: Session, _start: int = 0, _end: int = 100, _order: str = "ASC", _sort: str = "id"):
    desks_id = getattr(models.Desk, _sort).asc() if _order.upper(
    ) == "ASC" else getattr(models.Desk, _sort).desc()
    return db.query(models.Desk).order_by(desks_id).offset(_start).limit(_end).all()


def create_desk(db: Session, desk: schemas.DeskCreate):
    db_desk = models.Desk(
        number=desk.number, room_id=desk.room_id)
    db.add(db_desk)
    db.commit()
    db.refresh(db_desk)
    return db_desk


def update_desk(db: Session, desk: models.Desk, updates: schemas.DeskUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(desk, key, value)
    db.commit()
    updated_desk = get_user(db, desk.id)
    return updated_desk


def delete_desk(db: Session, desk_id: int):
    db.query(models.Desk).filter(models.Desk.id == desk_id).delete()
    db.commit()


def get_booking(db: Session, date: datetime.date, user_id: str):
    user_info = get_user(db, user_id=user_id)
    return db.query(models.Booking).filter(and_(models.Booking.date == date, models.Booking.user_id == user_info.id)).first()


def get_booking_by_desk_and_date(db: Session, desk_number: int, date: datetime.date, room_id: str):
    try:
        desk_info = db.query(models.Desk).filter(
            and_(models.Desk.number == desk_number, models.Desk.room_id == room_id)).one()
        return db.query(models.Booking).filter(and_(models.Booking.desk_id == desk_info.id, models.Booking.date == date)).first()
    except NoResultFound:
        return None


def get_bookings(db: Session, _start: int = 0, _end: int = 100, _order: str = "ASC", _sort: str = "id"):
    bookings_id = getattr(models.Booking, _sort).asc() if _order.upper(
    ) == "ASC" else getattr(models.Booking, _sort).desc()
    return db.query(models.Booking).order_by(bookings_id).offset(_start).limit(_end).all()


def create_booking(db: Session, booking: schemas.BookingCreate):
    try:
        user_info = db.query(models.User).filter(
            models.User.username == booking.username).one()
        desk_info = db.query(models.Desk).filter(and_(
            models.Desk.number == booking.desk_number, models.Desk.room_id == booking.room_id)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User or Desk not found")

    db_booking = models.Booking(
        user_id=user_info.id, desk_id=desk_info.id, date=booking.date, approved_status=booking.approved_status)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking: models.Booking, updates: schemas.BookingUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(booking, key, value)
    db.commit()
    updated_booking = get_user(db, booking.id)
    return updated_booking


def delete_desk(db: Session, booking_id: int):
    db.query(models.Booking).filter(models.Booking.id == booking_id).delete()
    db.commit()

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


def get_users(db: Session, range: list[int] = [0, 9], sort: list[str] = ["id", "ASC"]):
    users_id = getattr(models.User, sort[0]).asc() if sort[1].upper(
    ) == "ASC" else getattr(models.User, sort[0]).desc()
    return db.query(models.User).order_by(users_id).offset(range[0]).limit(range[1]).all()


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


def get_rooms(db: Session, range: list[int] = [0, 9], sort: list[str] = ["id", "ASC"]):
    rooms_id = getattr(models.Room, sort[0]).asc() if sort[1].upper(
    ) == "ASC" else getattr(models.Room, sort[0]).desc()
    return db.query(models.Room).order_by(rooms_id).offset(range[0]).limit(range[1]).all()


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
    updated_room = get_room(db, room.id)
    return updated_room


def delete_room(db: Session, room_id: int):
    db.query(models.Room).filter(models.Room.id == room_id).delete()
    db.commit()


def get_desk(db: Session, desk_id: int):
    return db.query(models.Desk).filter(models.Desk.id == desk_id).first()


def get_desk_by_room_and_number(db: Session, desk_number: int, room_id: int):
    return db.query(models.Desk).filter(and_(models.Desk.room_id == room_id, models.Desk.number == desk_number)).first()


def get_desks(db: Session, range: list[int] = [0, 9], sort: list[str] = ["id", "ASC"]):
    desks_id = getattr(models.Desk, sort[0]).asc() if sort[1].upper(
    ) == "ASC" else getattr(models.Desk, sort[0]).desc()
    return db.query(models.Desk).order_by(desks_id).offset(range[0]).limit(range[1]).all()


def get_desks_in_room(db: Session, room_id: int):
    desks_number = getattr(models.Desk, "number").asc()
    return db.query(models.Desk).filter(models.Desk.room_id == room_id).order_by(desks_number).all()


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
    updated_desk = get_desk(db, desk.id)
    return updated_desk


def delete_desk(db: Session, desk_id: int):
    db.query(models.Desk).filter(models.Desk.id == desk_id).delete()
    db.commit()


def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()


def get_booking_by_desk_and_date(db: Session, desk_id: int, date: datetime.date):
    try:
        return db.query(models.Booking).filter(and_(models.Booking.desk_id == desk_id, models.Booking.date == date)).first()
    except NoResultFound:
        return None


def get_bookings(db: Session, range: list[int] = [0, 9], sort: list[str] = ["id", "ASC"]):
    bookings_id = getattr(models.Booking, sort[0]).asc() if sort[1].upper(
    ) == "ASC" else getattr(models.Booking, sort[0]).desc()
    return db.query(models.Booking).order_by(bookings_id).offset(range[0]).limit(range[1]).all()


def get_bookings_by_room(db: Session, room_id: int, date: datetime.date):
    try:
        print("HERE")
        print(str(db.query(models.Booking).join(models.Desk).filter(and_(models.Desk.room_id == room_id, models.Booking.date == date.isoformat())).all()))
        return db.query(models.Booking).join(models.Desk).filter(and_(models.Desk.room_id == room_id, models.Booking.date == date.isoformat())).all()
    except NoResultFound:
        return None


def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(
        user_id=booking.user_id, desk_id=booking.desk_id, date=booking.date, approved_status=booking.approved_status)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking: models.Booking, updates: schemas.BookingUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(booking, key, value)
    db.commit()
    updated_booking = get_booking(db, booking.id)
    return updated_booking


def delete_booking(db: Session, booking_id: int):
    db.query(models.Booking).filter(models.Booking.id == booking_id).delete()
    db.commit()

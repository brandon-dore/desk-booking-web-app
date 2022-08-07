from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

import datetime

from api import models, schemas, auth

from datetime import datetime


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # Do hashing here
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=auth.get_hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_team_by_name(db: Session, team_name: str):
    return db.query(models.Team).filter(models.Team.name == team_name).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_room(db: Session, room_id: int):
    return db.query(models.Desk).filter(models.Room.id == room_id).first()


def get_room_by_name(db: Session, room_name: str):
    return db.query(models.Room).filter(models.Room.name == room_name).first()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_desk(db: Session, desk_id: int):
    return db.query(models.Desk).filter(models.Desk.id == desk_id).first()


def get_desk_by_room_and_number(db: Session, desk_number: int, room_name: str):
    return db.query(models.Desk).filter(and_(models.Desk.room == room_name, models.Desk.number == desk_number)).first()


def get_desks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Desk).offset(skip).limit(limit).all()


def create_desk(db: Session, desk: schemas.DeskCreate):
    db_desk = models.Desk(
        number=desk.number, room=desk.room, assigned_team=desk.assigned_team)
    db.add(db_desk)
    db.commit()
    db.refresh(db_desk)
    return db_desk


def get_booking(db: Session, date: datetime.date, user_email: str):
    user_info = get_user(db, email=user_email)
    return db.query(models.Booking).filter(and_(models.Booking.date == date, models.Booking.user_id == user_info.id)).first()


def get_booking_by_desk_and_date(db: Session, desk_number: int, date: datetime.date, room_name: str):
    try:
        desk_info = db.query(models.Desk).filter(
            and_(models.Desk.number == desk_number, models.Desk.room == room_name)).one()
        return db.query(models.Booking).filter(and_(models.Booking.desk_id == desk_info.id, models.Booking.date == date)).first()
    except NoResultFound:
        return None


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: schemas.BookingCreate):
    try:
        user_info = db.query(models.User).filter(
            models.User.email == booking.user_email).one()
        desk_info = db.query(models.Desk).filter(and_(
            models.Desk.number == booking.desk_number, models.Desk.room == booking.room_name)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User or Desk not found")

    db_booking = models.Booking(
        user_id=user_info.id, desk_id=desk_info.id, date=booking.date, approved_status=booking.approved_status)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

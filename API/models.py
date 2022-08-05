import uuid

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    # Possibly want to do UUID/GUID for users :)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, unique=False, nullable=False)
    hashed_password = Column(String(128))

    assigned_team = Column(Integer, ForeignKey(
        'teams.id'), unique=False, nullable=True)


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User")
    desks = relationship("Desk")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    desks = relationship("Desk")


class Desk(Base):
    __tablename__ = "desks"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)

    room = Column(String, ForeignKey(
        'rooms.name'), unique=False, nullable=False)

    assigned_team = Column(String, ForeignKey(
        'teams.name'), unique=False, nullable=True)

    __table_args__ = (UniqueConstraint(
        'number', 'room', name='_desk_room_uc'),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey(
        'users.id'), unique=False, nullable=False)
    desk_id = Column(Integer, ForeignKey(
        'desks.id'), unique=False, nullable=False)

    date = Column(Date, unique=False, nullable=False)
    approved_status = Column(Boolean, unique=False, nullable=False)
    
    desk = relationship("Desk")



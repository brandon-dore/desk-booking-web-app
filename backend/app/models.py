import uuid

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Defines each database table

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String(128))
    admin = Column(Boolean, unique=False, nullable=False)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Used for referencing relationships in SQLAlchemy, doesn't affect real DB
    desks = relationship("Desk")


class Desk(Base):
    __tablename__ = "desks"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)

    room_id = Column(Integer, ForeignKey(
        'rooms.id'), unique=False, nullable=False)

    # Stops duplicates by only allowing unique combinations of room and desk
    __table_args__ = (UniqueConstraint(
        'number', 'room_id', name='_desk_room_uc'),
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
    user = relationship("User")

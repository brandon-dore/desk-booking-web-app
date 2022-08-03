import uuid

from uuid import UUID
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

users_events = Table('user_booking',
                        Column('user_id', UUID(as_uuid=True),
                                  ForeignKey('user.id')),
                        Column('booking_id', UUID(as_uuid=True),
                                  ForeignKey('booking.id'))
                        )

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String(128))
    assigned_team = Column(UUID(as_uuid=True), ForeignKey(
        'team.id'), unique=False, nullable=True)

    
class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    members = relationship('User', backref='team')

class Desk(Base):
    __tablename__ = "desks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    desk_number = Column(Integer, unique=True, nullable=False)
    assigned_team = Column(UUID(as_uuid=True), ForeignKey(
        'team.id'), unique=False, nullable=True)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    approved_status = Column(Boolean, unique=False, nullable=False)
    start_date = Column(Date, unique=False, nullable=False)
    end_date = Column(Date, unique=False, nullable=False)
    assigned_desk = Column(UUID(as_uuid=True), ForeignKey(
        'desk.id'), unique=False, nullable=False)
    users = relationship('User', secondary=users_events, backref='events')
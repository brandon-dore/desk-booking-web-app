import uuid

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

users_teams = Table('user_team',
                    Base.metadata,
                    Column('user_id', Integer,
                           ForeignKey('users.id')),
                    Column('team_id', Integer,
                           ForeignKey('teams.id'))
                    )

teams_desks = Table('teams_desk',
                    Base.metadata,
                    Column('team_id', Integer,
                           ForeignKey('teams.id')),
                    Column('desk_id', Integer,
                           ForeignKey('desks.id'))
                    )


class User(Base):
    __tablename__ = "users"

    # Possibly want to do UUID/GUID for users :)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, unique=False, nullable=False)
    hashed_password = Column(String(128))


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Desk(Base):
    __tablename__ = "desks"

    id = Column(Integer, primary_key=True, index=True)
    desk_number = Column(Integer, nullable=False)
    room_name = Column(String, nullable=False)
    assigned_team = Column(Integer, ForeignKey(
        'teams.id'), unique=False, nullable=True)

    __table_args__ = (UniqueConstraint(
        'desk_number', 'room_name', name='_desk_room_uc'),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    approved_status = Column(Boolean, unique=False, nullable=False)
    start_date = Column(Date, unique=False, nullable=False)
    end_date = Column(Date, unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id'), unique=False, nullable=False)
    desk_id = Column(Integer, ForeignKey(
        'desks.id'), unique=False, nullable=False)

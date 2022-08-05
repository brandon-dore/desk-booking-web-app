from typing import Dict, Union, List, Tuple

from uuid import UUID
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pass

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    pass

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    name: str


class RoomCreate(TeamBase):
    pass


class Room(TeamBase):
    pass

    class Config:
        orm_mode = True

class DeskBase(BaseModel):
    number: int
    room: str
    assigned_team: str


class DeskCreate(DeskBase):
    pass


class Desk(DeskBase):
    pass

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    approved_status: bool
    date: datetime.date

class BookingCreate(BookingBase):
    desk_number: int
    user_email: str
    room_name: str

class Booking(BookingBase):
    desk: Desk

    class Config:
        orm_mode = True
        
class Overview(BaseModel):
    booking: Booking
    desk: Desk


    class Config:
        orm_mode = True


class UserOut(UserBase):
    authors: List[TeamBase]


class TeamOutUsers(TeamBase):
    books: List[UserBase]


class TeamOutDesks(TeamBase):
    authors: List[DeskBase]


class DeskOut(DeskBase):
    books: List[DeskBase]
    
class JoinResult(BaseModel):
    results: List[Tuple[Booking, Desk]]

    class Config:
        orm_mode = True
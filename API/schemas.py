from typing import Union, List
from uuid import UUID
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class DeskBase(BaseModel):
    desk_number: int
    room_name: str
    assigned_team: int


class DeskCreate(DeskBase):
    pass


class Desk(DeskBase):
    id: int

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    approved_status: str
    start_date: datetime.date
    end_date: datetime.date


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True


class UserSchema(UserBase):
    authors: List[TeamBase]


class UTeamSchema(TeamBase):
    books: List[UserBase]


class DTeamSchema(TeamBase):
    authors: List[DeskBase]


class DeskSchema(DeskBase):
    books: List[DeskBase]

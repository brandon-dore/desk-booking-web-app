from typing import List, Tuple, Union

import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    assigned_team: str = None


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
    assigned_team: str = None


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
    username: str
    room_name: str


class Booking(BookingBase):
    desk: Desk
    user: User

    class Config:
        orm_mode = True


class Overview(BaseModel):
    booking: Booking
    desk: Desk

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


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

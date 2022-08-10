from typing import List, Tuple, Union

import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    assigned_team: Union[str, None] = None
    admin: bool = False


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


class RoomBase(BaseModel):
    name: str


class RoomCreate(TeamBase):
    pass


class Room(TeamBase):
    id: int

    class Config:
        orm_mode = True


class DeskBase(BaseModel):
    number: int
    room: str
    assigned_team: Union[str, None] = None


class DeskCreate(DeskBase):
    pass


class Desk(DeskBase):
    id: int

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
    id: int
    desk_id: int
    user_id: int

    class Config:
        orm_mode = True

class BookingSummary(BookingBase):
    id: int
    desk: Desk
    user: User

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

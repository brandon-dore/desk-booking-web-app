from typing import List, Tuple, Union

import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    admin: Union[bool, None] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    admin: Union[bool, None] = None

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True


class RoomUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class DeskBase(BaseModel):
    number: int
    room_id: int


class DeskCreate(DeskBase):
    pass


class Desk(DeskBase):
    id: int

    class Config:
        orm_mode = True


class DeskUpdate(BaseModel):
    number: Union[int, None] = None
    room_id: Union[int, None] = None

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    approved_status: bool
    date: datetime.date


class BookingCreate(BookingBase):
    desk_number: int
    username: str
    room_id: int


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


class BookingUpdate(BaseModel):
    desk_id: Union[int, None] = None
    username: Union[str, None] = None
    user_id: Union[int, None] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class DeskOut(DeskBase):
    books: List[DeskBase]


class JoinResult(BaseModel):
    results: List[Tuple[Booking, Desk]]

    class Config:
        orm_mode = True

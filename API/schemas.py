from typing import Union
from uuid import UUID
import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    team_id: UUID

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    
class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: UUID

    class Config:
        orm_mode = True

class DeskBase(BaseModel):
    number: int
    
class DeskCreate(DeskBase):
    assigned_team: UUID

class Desk(DeskBase):
    id: UUID

    class Config:
        orm_mode = True
    
class BookingBase(BaseModel):
    approved_status: str
    start_date: datetime.date
    end_date: datetime.date
    desk_id: UUID
    
class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: UUID

    class Config:
        orm_mode = True


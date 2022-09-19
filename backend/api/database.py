from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from api import models, security
from datetime import datetime


def add_data_to_db(db): # pragma: no cover
    db.add(models.User(
        email="admin@admin.com", username="admin", hashed_password=security.get_hashed_password("password"), admin=True))
    db.add(models.User(
        email="user", username="John Doe", hashed_password=security.get_hashed_password("test"), admin=True))

    db.add(models.Room(name="Room 431"))
    db.add(models.Room(name="Inspiration Station"))
    db.add(models.Room(name="The Hive"))

    for desk_number in range(0, 25):
        db.add(models.Desk(
            number=desk_number, room_id=1))
    for desk_number in range(5, 110, 5):
        db.add(models.Desk(
            number=desk_number, room_id=2))
    for desk_number in range(2, 8, 2):
        db.add(models.Desk(
            number=desk_number, room_id=3))

    db.add(models.Booking(
        user_id=2, desk_id=5, date=datetime.today().strftime('%Y-%m-%d'), approved_status=True))

    db.commit()


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/desk_booking_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
    models.Base.metadata.create_all(bind=engine)
    add_data_to_db(db)
else:
    models.Base.metadata.create_all(bind=engine)


Base = declarative_base()

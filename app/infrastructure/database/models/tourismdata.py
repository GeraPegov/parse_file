
from datetime import date
from sqlalchemy import BigInteger, Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.connection import Base


class TourismData(Base):
    __tablename__ = 'tourism'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    date_of_arrival: Mapped[date] = mapped_column(Date)
    trip_type: Mapped[str] = mapped_column(String)
    home_country: Mapped[str] = mapped_column(String)
    home_region: Mapped[str] = mapped_column(String)
    home_city: Mapped[str] = mapped_column(String)
    goal: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    age: Mapped[str] = mapped_column(String)
    income: Mapped[str] = mapped_column(String)
    days_cnt: Mapped[int] = mapped_column(Integer)
    visitors_cnt: Mapped[int] = mapped_column(Integer)
    spent: Mapped[float] = mapped_column(Float)
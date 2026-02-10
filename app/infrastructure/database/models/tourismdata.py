from datetime import date
from sqlalchemy import BigInteger, Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.connection import Base


class TourismData(Base):
    __tablename__ = "tourism"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    DATE_OF_ARRIVAL: Mapped[date | None] = mapped_column(Date)
    VISIT_TYPE: Mapped[str | None] = mapped_column(String(20))
    TRIP_TYPE: Mapped[str | None] = mapped_column(String(50))
    HOME_COUNTRY: Mapped[str | None] = mapped_column(String(50))
    HOME_REGION: Mapped[str | None] = mapped_column(String(50))
    HOME_CITY: Mapped[str | None] = mapped_column(String(50))
    GOAL: Mapped[str | None] = mapped_column(String(50))
    GENDER: Mapped[str | None] = mapped_column(String(10))
    AGE: Mapped[str | None] = mapped_column(String(50))
    INCOME: Mapped[str | None] = mapped_column(String(50))
    DAYS_CNT: Mapped[int | None] = mapped_column(Integer)
    VISITORS_CNT: Mapped[int | None] = mapped_column(Integer)
    SPENT: Mapped[float | None] = mapped_column(Float)

from sqlalchemy import desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.analysis_repository import IAnalysisRepository
from app.infrastructure.database.models.tourismdata import TourismData
from app.infrastructure.database.repositories.parse_repository import handle_db_errors


class AnalysisRepository(IAnalysisRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @handle_db_errors
    async def get_tourists_for_all_dates(self) -> dict:
        db_result = await self.session.execute(
            select(func.sum(TourismData.VISITORS_CNT))
        )

        rows = db_result.scalar_one()

        return {"Количество туристов за все даты": int(rows)}

    @handle_db_errors
    async def get_tourists_for_every_month(self) -> dict:
        db_result = await self.session.execute(
            select(
                func.to_char(TourismData.DATE_OF_ARRIVAL, "YYYY-MM").label("month"),
                func.sum(TourismData.VISITORS_CNT).label("tourists_count"),
            ).group_by("month")
        )
        rows = db_result.all()
        tourists_by_month = {"Количество туристов за периоды": []}
        for row in rows:
            date_visit, quantity = row
            if isinstance(date_visit, str):
                tourists_by_month["Количество туристов за периоды"].append(
                    {"Дата": date_visit, "Количество": int(quantity)}
                )

        return tourists_by_month

    @handle_db_errors
    async def get_tourists_for_random_period(self) -> dict:
        random_date_subquery = (
            select(TourismData.DATE_OF_ARRIVAL).order_by(func.random()).limit(1)
        ).scalar_subquery()

        limit_records = (
            select(
                TourismData.DATE_OF_ARRIVAL.label("date"),
                func.sum(TourismData.VISITORS_CNT).label("sum_visitors"),
            )
            .where(TourismData.DATE_OF_ARRIVAL >= random_date_subquery)
            .group_by(TourismData.DATE_OF_ARRIVAL)
            .order_by(TourismData.DATE_OF_ARRIVAL)
            .limit(10)
            .subquery()
        )

        db_result = await self.session.execute(
            select(
                func.min(limit_records.c.date),
                func.max(limit_records.c.date),
                func.sum(limit_records.c.sum_visitors),
            )
        )
        row = db_result.one()

        first_date, last_date, sum_of_period = row
        tourists_by_random_period = {
            "Количество посетителей за рандомный промежуток": []
        }
        tourists_by_random_period[
            "Количество посетителей за рандомный промежуток"
        ].append(
            {
                "Дата от:": first_date.isoformat(),
                "До:": last_date.isoformat(),
                "Количество человек:": int(sum_of_period),
            }
        )
        return tourists_by_random_period

    @handle_db_errors
    async def get_tourists_by_country(self) -> dict:
        db_result = await self.session.execute(
            select(
                TourismData.HOME_COUNTRY, func.sum(TourismData.VISITORS_CNT)
            ).group_by(TourismData.HOME_COUNTRY)
        )

        rows = db_result.all()
        tourists_by_country = {"Территориальное распределение по странам": []}

        for row in rows[1:]:
            country, quantity = row
            if quantity != 0:
                tourists_by_country["Территориальное распределение по странам"].append(
                    {"Страна": country, "Количество посетителей": int(quantity)}
                )
        return tourists_by_country

    @handle_db_errors
    async def get_tourists_by_region(self) -> dict:
        db_result = await self.session.execute(
            select(
                TourismData.HOME_REGION, func.sum(TourismData.VISITORS_CNT)
            ).group_by(TourismData.HOME_REGION)
        )

        rows = db_result.all()
        tourists_by_region = {"Территориальное распределение по регионам": []}

        for row in rows[1:]:
            region, quantity = row
            if quantity != 0:
                tourists_by_region["Территориальное распределение по регионам"].append(
                    {"Регион": region, "Количество посетителей": int(quantity)}
                )
        return tourists_by_region

    @handle_db_errors
    async def get_demographic_distribution(self) -> dict:
        db_result = await self.session.execute(
            select(
                TourismData.AGE, TourismData.GENDER, func.sum(TourismData.VISITORS_CNT)
            ).group_by(TourismData.AGE, TourismData.GENDER)
        )

        rows = db_result.all()
        demographic_distribution = {"Демографическое распределение": []}

        for row in rows[1:]:
            age, gender, quantity = row
            if quantity != 0:
                demographic_distribution["Демографическое распределение"].append(
                    {"Возраст": age, "Пол": gender, "Количество": quantity}
                )

        return demographic_distribution

    @handle_db_errors
    async def get_typical_tourist_profile(self) -> dict:
        db_result = await self.session.execute(
            select(
                func.avg(TourismData.SPENT).label("avg_spent"),
                func.avg(TourismData.DAYS_CNT).label("avg_days"),
                func.count(TourismData.id).label("quantity_records"),
                TourismData.INCOME,
                TourismData.AGE,
            )
            .group_by(TourismData.AGE, TourismData.INCOME)
            .order_by(desc("quantity_records"))
            .limit(1)
        )
        rows = db_result.all()
        typical_tourist_profile = {}

        for row in rows:
            spent, days, quantity, income, age = row
            typical_tourist_profile["Профиль среднестатестического туриста"] = {
                "Траты в городе на сумму": int(spent * 1000000),
                "Количество дней в городе": int(days),
                "Доход туриста": income,
                "Возраст": age,
            }

        return typical_tourist_profile

    @handle_db_errors
    async def get_most_valuable_segments(self) -> dict:
        db_result = await self.session.execute(
            select(
                func.count(TourismData.id).label("count_id"),
                func.sum(TourismData.VISITORS_CNT).label("sum_visitors"),
                TourismData.AGE.label("age"),
                func.avg(TourismData.DAYS_CNT).label("avg_days"),
                func.avg(TourismData.SPENT).label("avg_spent"),
            )
            .where(TourismData.GOAL == "Туризм")
            .group_by("age")
            .order_by(desc("count_id"))
            .limit(3)
        )
        rows = db_result.all()
        valuable_segments = {"Популярные категории туристов": []}
        for row in rows:
            quantity, visitors, age, avg_days, avg_spent = row
            valuable_segments["Популярные категории туристов"].append(
                {
                    "Возрастная категория": age,
                    "Количество туристов": visitors,
                    "Среднее количество дней в городе": int(avg_days),
                    "Средняя сумма трат в городе": int(avg_spent * 1000000),
                }
            )

        return valuable_segments

import random
from sqlalchemy import desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.analysis_repository import IAnalysisRepository
from app.infrastructure.database.models.tourismdata import TourismData

class AnalysisRepository(IAnalysisRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def tourists_for_all_dates(self) -> dict:
        data_orm = await self.session.execute(
            select(func.sum(TourismData.VISITORS_CNT))
        )

        data = data_orm.scalar_one()

        return {"Количество туристов за все даты": int(data)}
    

    async def tourists_for_every_month(self) -> dict:
        data_orm = await self.session.execute(
            select(
                func.to_char(TourismData.DATE_OF_ARRIVAL, 'YYYY-MM').label('month'),
                func.sum(TourismData.VISITORS_CNT).label('tourists_count')
            ).group_by('month')
        )
        data = data_orm.all()
        dict_response = {'Количество туристов за периоды': []}
        for record in data:
            date_visit, quantity = record
            if isinstance(date_visit, str):
                dict_response['Количество туристов за периоды'].append({
                    "Дата" : date_visit,
                    "Количество": int(quantity)
                })
            
        return dict_response


    async def tourists_for_random_period(self):

        random_date_subquery = (
            select(TourismData.DATE_OF_ARRIVAL)
            .order_by(func.random())
            .limit(1)
        ).scalar_subquery()

        query = select(
                TourismData.DATE_OF_ARRIVAL.label('date'),
                func.sum(TourismData.VISITORS_CNT).label('sum_visitors')
            ).where(
                TourismData.DATE_OF_ARRIVAL >= random_date_subquery
            ).group_by(
                TourismData.DATE_OF_ARRIVAL
            ).order_by(
                TourismData.DATE_OF_ARRIVAL
            ).limit(
                10
            ).subquery()
        
        data_orm = await self.session.execute(
            select(
                func.min(query.c.date),
                func.max(query.c.date),
                func.sum(query.c.sum_visitors)
            )
        )
        data = data_orm.one()

        first_date, last_date, sum_of_period = data
        dict_response = {"Количество посетителей за рандомный промежуток": []}
        dict_response["Количество посетителей за рандомный промежуток"].append({
            'Дата от:': first_date.isoformat(),
            'До:': last_date.isoformat(),
            'Количество человек:': int(sum_of_period)
        })
        return dict_response


    async def from_country(self):
        data_orm = await self.session.execute(
            select(
                TourismData.HOME_COUNTRY,
                func.sum(TourismData.VISITORS_CNT))
                .group_by(TourismData.HOME_COUNTRY)
        )

        data = data_orm.all()
        response_dict = {"Территориальное распределение по странам": []}

        for i in data[1:]:
            country, quantity = i
            if quantity != 0:
                response_dict["Территориальное распределение по странам"].append({
                    "Страна": country,
                    "Количество посетителей": int(quantity)
                    })
        return response_dict


    async def from_region(self):
        data_orm = await self.session.execute(
            select(
                TourismData.HOME_REGION,
                func.sum(TourismData.VISITORS_CNT))
                .group_by(TourismData.HOME_REGION)
        )

        data = data_orm.all()
        response_dict = {"Территориальное распределение по регионам": []}

        for i in data[1:]:
            region, quantity = i
            if quantity != 0:
                response_dict["Территориальное распределение по регионам"].append({
                    "Регион": region,
                    "Количество посетителей": int(quantity)
                })
        return response_dict


    async def demographic_presentation(self):
        data_orm = await self.session.execute(
            select(
                TourismData.AGE,
                TourismData.GENDER,
                func.sum(TourismData.VISITORS_CNT)
                )
            .group_by(TourismData.AGE, TourismData.GENDER)
        )

        data = data_orm.all()
        response_dict = {"Демографическое распределение": []}

        for i in data[1:]:
            age, gender, quantity = i
            if quantity != 0:
                response_dict["Демографическое распределение"].append({
                    'Возраст': age,
                    'Пол': gender,
                    'Количество': quantity
                    })
            
        return response_dict
    

    async def average_tourists(self):
        data_orm = await self.session.execute(select(
                func.avg(TourismData.SPENT).label('avg_spent'),
                func.avg(TourismData.DAYS_CNT).label('avg_days'),
                func.count(TourismData.id).label('quantity_records'),
                TourismData.INCOME,
                TourismData.AGE
            ).group_by(TourismData.AGE, TourismData.INCOME)\
            .order_by(desc('quantity_records')).limit(1))
        
        response_dict = {}

        for item in data_orm.all():
            spent, days, quantity, income, age = item
            response_dict['Профиль среднестатестического туриста'] = {
                'Траты в городе на сумму': int(spent*1000000),
                'Количество дней в городе': int(days),
                'Доход туриста': income,
                'Возраст': age,
            }
        
        return response_dict
    

    async def profit_event(self):
        data_orm = await self.session.execute(\
            select(
                func.count(TourismData.id).label('count_id'),
                func.sum(TourismData.VISITORS_CNT).label('sum_visitors'),
                TourismData.AGE.label('age'),
                func.avg(TourismData.DAYS_CNT).label('avg_days'),
                func.avg(TourismData.SPENT).label('avg_spent')
            ).where(TourismData.GOAL=='Туризм').group_by('age')\
            .order_by(desc('count_id')).limit(3))

        response_dict = {'Популярные категории туристов': []}
        for item in data_orm.all():
            quantity, visitors, age, avg_days, avg_spent = item 
            response_dict['Популярные категории туристов'].append({
                'Возрастная категория': age,
                'Количество туристов': visitors,
                'Среднее количество дней в городе': int(avg_days),
                'Средняя сумма трат в городе': int(avg_spent*1000000)
            })

        return response_dict
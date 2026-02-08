from datetime import date
from re import sub
from sqlalchemy import select, func
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

        return {"Количество туристов за все даты": data}
    

    async def tourists_for_every_month(self) -> dict:
        data_orm = await self.session.execute(
            select(
                func.to_char(TourismData.DATE_OF_ARRIVAL, 'YYYY-MM').label('month'),
                func.sum(TourismData.VISITORS_CNT).label('tourists_count')
            ).group_by('month')
        )
        data = data_orm.all()
        dict_response = {}
        for record in data:
            date_visit, quantity = record
            print(type(date_visit))
            if isinstance(date_visit, str):
                dict_response[date_visit] = quantity
            
        return dict_response

    async def tourists_for_random_period(self):
        subquery = select(
            TourismData.DATE_OF_ARRIVAL.label('date'),
            func.sum(TourismData.VISITORS_CNT).label('visitors_sum')
            ).group_by(TourismData.DATE_OF_ARRIVAL).order_by(func.random()).limit(10).subquery()
        
        request = await self.session.execute(
            select(
                func.max(subquery.c.date).label('last_date'),
                func.min(subquery.c.date).label('first_date'),
                func.sum(subquery.c.visitors_sum).label('sum')
                )
        )
        first_date, last_date, sum_of_period = request.all()
        dict_response = {
            'Дата от:': first_date,
            'До:': last_date,
            'Количество человек за период:': sum_of_period
        }
        return dict_response
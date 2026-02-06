import io
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import numpy as np

from app.infrastructure.database.repositories.tourism_repository import TourismRepository


class TourismService:
    def __init__(self, repo: TourismRepository):
        self.repo = repo

    
    def clean_chunk(self, df: pd.DataFrame):
        df = df.drop_duplicates()
        for column in df.columns:
            df[column] = df[column].astype(str)\
                .str.replace(r'[\x00-\x1f\x7f-\x9f]', '', regex=True)\
                .str.strip()\
                .replace(['', 'nan', 'None', 'null'], np.nan)

            if df[column].notna().sum() == 0:
                df = df.drop(columns=[column])
                continue

            first_valid = df[column].dropna().iloc[0]
            df[column] = df[column].fillna(first_valid)\
                                    .astype(str)

            result = np.where((df[column] != df[column].iloc[0]) & (df[column] != column))
            if len(result[0]) == 0:
                df = df.drop(columns=[column])

        if 'DAYS_CNT' in df.columns:
            df['DAYS_CNT'] = pd.to_numeric(df["DAYS_CNT"], errors='coerce')
        if 'VISITORS_CNT' in df.columns:
            df['VISITORS_CNT'] = pd.to_numeric(df["VISITORS_CNT"], errors='coerce')
        if 'SPENT' in df.columns:
            df['SPENT'] = pd.to_numeric(df["SPENT"], errors='coerce').astype(float)
        if 'DATE_OF_ARRIVAL' in df.columns:
            df['DATE_OF_ARRIVAL'] = pd.to_datetime(df['DATE_OF_ARRIVAL'], errors='coerce')
        return df

    '''
    Сначала привели типы numpy для валидации исключений(NaN, пробелы и прочие ошибки)
    Затем создали новый список словарей с приведением пайтон типов
    Через isinstance мы исключили возможность приведение NaN к типу
    '''
    async def parse_file(self, file: bytes, chunk_size: int = 50000):
     
        data = io.BytesIO(file)

        for chunk in pd.read_csv(data, chunksize=chunk_size):
            result = self.clean_chunk(chunk)

            records = result.to_dict('records')
            cleaned = []
            for record in records:
                cleaned_rec = {}
                for key, value in record.items():
                    key_lower = key.lower()
                    if pd.isna(value):
                        cleaned_rec[key_lower] = None
                    elif isinstance(value, np.integer):
                        cleaned_rec[key_lower] = int(value)
                    elif isinstance(value, np.floating):
                        cleaned_rec[key_lower] = float(value)
                    elif isinstance(value, pd.Timestamp):
                        cleaned_rec[key_lower] = value.date()
                    else:
                        cleaned_rec[key_lower] = str(value)
                cleaned.append(cleaned_rec)
        
            await self.repo.save(cleaned)
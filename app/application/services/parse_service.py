import io
import pandas as pd
import numpy as np


from app.domain.interfaces.parse_repository import IParseRepository


class ParseService:
    def __init__(self, repo: IParseRepository):
        self.repo = repo

    def clean_chunk(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates()
        for column_name in df.columns:
            df[column_name] = (
                df[column_name]
                .astype(str)
                .str.replace(r"[\x00-\x1f\x7f-\x9f]", "", regex=True)
                .str.strip()
                .replace(["", "nan", "None", "null"], np.nan)
            )

            if df[column_name].notna().sum() == 0:
                df = df.drop(columns=[column_name])
                continue

            first_valid = df[column_name].dropna().iloc[0]
            df[column_name] = df[column_name].fillna(first_valid).astype(str)
            is_different = (df[column_name] != df[column_name].iloc[0]) & (
                df[column_name] != column_name
            )
            if not is_different.any():
                df = df.drop(columns=[column_name])

        self._convert_column_types(df)
        return df

    def _convert_column_types(self, df: pd.DataFrame) -> None:
        type_conversions = {
            "DAYS_CNT": lambda col: pd.to_numeric(col, errors="coerce"),
            "VISITORS_CNT": lambda col: pd.to_numeric(col, errors="coerce"),
            "SPENT": lambda col: pd.to_numeric(col, errors="coerce").astype(float),
            "DATE_OF_ARRIVAL": lambda col: pd.to_datetime(col, errors="coerce"),
        }

        for column_name, converter in type_conversions.items():
            if column_name in df.columns:
                df[column_name] = converter(df[column_name])

    async def parse_file(self, file: bytes, chunk_size: int = 2500) -> dict | None:
        data = io.BytesIO(file)
        data.seek(0)
        for chunk in pd.read_csv(data, chunksize=chunk_size, encoding="utf-8"):
            result = self.clean_chunk(chunk)

            records = result.to_dict("records")
            normalized_records = self._normalize_records(records)
            if normalized_records:
                status = await self.repo.save(normalized_records)
        return status

    def _normalize_records(self, records: list[dict]) -> list[dict]:
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, (np.integer, int)):
                    record[key] = int(value)
                elif isinstance(value, (np.floating, float)):
                    record[key] = float(value)
                elif isinstance(value, pd.Timestamp):
                    record[key] = value.date()

        return records

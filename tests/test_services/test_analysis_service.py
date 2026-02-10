# tests/test_services/test_parse_service.py
import pytest
import pandas as pd
import numpy as np
from datetime import date
from app.application.services.parse_service import ParseService


class TestParseService:
    def setup_method(self):
        self.service = ParseService(repo=None)

    def test_clean_chunk_removes_duplicates(self):
        df = pd.DataFrame({'A': [1, 1, 2, 3]})
        
        result = self.service.clean_chunk(df)
        
        assert len(result) == 3

    def test_clean_chunk_removes_empty_columns(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [np.nan, np.nan, np.nan]
        })
        
        result = self.service.clean_chunk(df)
        
        assert 'B' not in result.columns

    def test_clean_chunk_fills_missing_values(self):
        df = pd.DataFrame({'A': ['first', np.nan, 'third']})
        
        result = self.service.clean_chunk(df)
        
        assert result['A'].iloc[1] == 'first'

    def test_clean_chunk_removes_constant_columns(self):
        df = pd.DataFrame({
            'A': ['same', 'same', 'same'],
            'B': [1, 2, 3]
        })
        
        result = self.service.clean_chunk(df)
        
        assert 'A' not in result.columns
        assert 'B' in result.columns

    def test_convert_column_types_days_cnt(self):
        df = pd.DataFrame({'DAYS_CNT': ['5', '10', '15']})
        
        self.service._convert_column_types(df)
        
        assert df['DAYS_CNT'].iloc[0] == 5

    def test_normalize_records_nan_to_none(self):
        records = [{'A': np.nan, 'B': 5}]
        
        result = self.service._normalize_records(records)
        
        assert result[0]['A'] is None
        assert result[0]['B'] == 5

    def test_normalize_records_numpy_int_to_python_int(self):
        records = [{'count': np.int64(10)}]
        
        result = self.service._normalize_records(records)
        
        assert isinstance(result[0]['count'], int)
        assert result[0]['count'] == 10

    def test_normalize_records_numpy_float_to_python_float(self):
        records = [{'value': np.float64(3.14)}]
        
        result = self.service._normalize_records(records)
        
        assert isinstance(result[0]['value'], float)
        assert result[0]['value'] == 3.14

    def test_normalize_records_timestamp_to_date(self):
        records = [{'date': pd.Timestamp('2021-01-15')}]
        
        result = self.service._normalize_records(records)
        
        assert isinstance(result[0]['date'], date)
        assert result[0]['date'] == date(2021, 1, 15)
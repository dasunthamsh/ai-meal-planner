import pytest
import pandas as pd
import numpy as np
from models.data_preprocessor import DataPreprocessor
from unittest.mock import patch, mock_open

class TestDataPreprocessor:

    def test_initialization(self):
        """Test DataPreprocessor initialization"""
        preprocessor = DataPreprocessor()
        assert preprocessor.df is None
        assert preprocessor.scaler is not None
        assert preprocessor.vitamins is None
        assert preprocessor.diet_cols is None

    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        """Test successful data loading"""
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_read_csv.return_value = mock_df

        preprocessor = DataPreprocessor()
        result = preprocessor.load_data()

        mock_read_csv.assert_called_once()
        assert preprocessor.df is not None
        assert isinstance(result, pd.DataFrame)

    @patch('pandas.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        """Test data loading with file not found"""
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        preprocessor = DataPreprocessor()

        with pytest.raises(FileNotFoundError):
            preprocessor.load_data()

    def test_preprocess_data_with_sample_data(self, sample_meal_data):
        """Test data preprocessing with sample data"""
        preprocessor = DataPreprocessor()
        preprocessor.df = sample_meal_data

        df_processed, scaler, vitamins, diet_cols = preprocessor.preprocess_data()

        # Check if preprocessing was successful
        assert df_processed is not None
        assert scaler is not None
        assert isinstance(vitamins, list)
        assert isinstance(diet_cols, list)

        # Check if numerical columns are normalized
        nutrition_cols = ['calories', 'protein', 'fat', 'carbs']
        for col in nutrition_cols:
            if col in df_processed.columns:
                assert df_processed[col].max() <= 1.0
                assert df_processed[col].min() >= 0.0

    def test_preprocess_data_missing_columns(self):
        """Test preprocessing with missing required columns"""
        preprocessor = DataPreprocessor()
        preprocessor.df = pd.DataFrame({'meal_name': ['Test Meal']})

        with pytest.raises(ValueError):
            preprocessor.preprocess_data()

    def test_validate_data_success(self, sample_meal_data):
        """Test data validation with complete data"""
        preprocessor = DataPreprocessor()
        preprocessor.df = sample_meal_data

        result = preprocessor.validate_data()
        assert result == True

    def test_validate_data_missing_columns(self):
        """Test data validation with missing columns"""
        preprocessor = DataPreprocessor()
        preprocessor.df = pd.DataFrame({'meal_name': ['Test']})

        result = preprocessor.validate_data()
        assert result == False

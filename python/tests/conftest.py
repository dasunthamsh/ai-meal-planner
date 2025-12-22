import pytest
import pandas as pd
import sys
import os
from unittest.mock import Mock, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_meal_data():
    """Sample meal data for testing"""
    return pd.DataFrame({
        'meal_name': ['Oatmeal', 'Grilled Chicken', 'Salmon Salad', 'Vegetable Stir Fry'],
        'calories': [150, 300, 400, 250],
        'protein': [5, 30, 25, 8],
        'fat': [3, 12, 20, 10],
        'carbs': [27, 5, 15, 30],
        'ingredients': ['oats, milk, honey', 'chicken, olive oil', 'salmon, greens, lemon', 'vegetables, soy sauce'],
        'image_url': ['url1', 'url2', 'url3', 'url4'],
        'vitamins': ['A, C', 'B6, B12', 'D, Omega3', 'A, C, K'],
        'sodium_mg': [50, 200, 300, 400],
        'sugar_g': [5, 2, 3, 4],
        'fiber_g': [4, 1, 2, 5],
        'cholesterol_mg': [0, 80, 60, 0],
        'saturated_fat_g': [0.5, 2, 3, 1],
        'omega3_g': [0, 0, 1.2, 0],
        'vegetarian': [1, 0, 0, 1],
        'vegan': [0, 0, 0, 1],
        'gluten_free': [1, 1, 1, 0]
    })

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        'adjustedCalories': 2000,
        'goal': 'Lose Weight',
        'dietType': 'Vegetarian',
        'allergies': ['dairy'],
        'healthRisks': ['High blood pressure'],
        'days': 7
    }

@pytest.fixture
def target_nutrition():
    """Sample target nutrition data"""
    return {
        'calories': 2000,
        'protein': 175,  # (2000 * 0.35) / 4
        'fat': 55.6,     # (2000 * 0.25) / 9
        'carbs': 200     # (2000 * 0.40) / 4
    }

@pytest.fixture
def dietary_restrictions():
    """Sample dietary restrictions"""
    return {
        'vegetarian': True,
        'vegan': False,
        'keto': False,
        'paleo': False,
        'gluten_free': False,
        'mediterranean': False,
        'allergies': ['dairy'],
        'health_risks': ['High blood pressure']
    }

import pytest
from models.data_preprocessor import DataPreprocessor
from models.genetic_algorithm import MealPlanGeneticAlgorithm

class TestIntegration:

    def test_end_to_end_meal_generation(self, sample_meal_data, sample_user_data):
        """Test complete meal generation pipeline"""
        # Initialize components
        preprocessor = DataPreprocessor()
        preprocessor.df = sample_meal_data

        # Preprocess data
        df_processed, scaler, vitamins, diet_cols = preprocessor.preprocess_data()

        # Initialize genetic algorithm
        ga = MealPlanGeneticAlgorithm(df_processed)

        # Define target nutrition
        target_nutrition = {
            'calories': 2000,
            'protein': 175,
            'fat': 55.6,
            'carbs': 200
        }

        # Define dietary restrictions
        dietary_restrictions = {
            'vegetarian': True,
            'vegan': False,
            'keto': False,
            'paleo': False,
            'gluten_free': False,
            'mediterranean': False,
            'allergies': ['dairy'],
            'health_risks': ['High blood pressure']
        }

        # Generate meal plan
        days = 3
        meal_plan = ga.evolve(target_nutrition, dietary_restrictions, days)

        # Verify results
        assert meal_plan is not None
        assert len(meal_plan) == days

        for day_meals in meal_plan:
            assert 'breakfast' in day_meals
            assert 'lunch' in day_meals
            assert 'dinner' in day_meals

            # Verify meal indices are valid
            for meal_type, meal_idx in day_meals.items():
                assert 0 <= meal_idx < len(df_processed)

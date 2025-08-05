import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
import os

class MealRecommender:
    def __init__(self, dataset_path='dataset/meal_dataset.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.preprocessor = None
        self.features = None
        self.meal_data = None

    def load_data(self):
        """Load and preprocess the meal dataset"""
        self.meal_data = pd.read_csv(self.dataset_path)

        # Clean data
        self.meal_data.dropna(inplace=True)
        self.meal_data = self.meal_data[self.meal_data['calories'] > 0]

        # Create feature columns
        self.meal_data['meal_type'] = self.meal_data['meal_name'].apply(
            lambda x: 'breakfast' if 'breakfast' in x.lower() else
                     'lunch' if 'lunch' in x.lower() else
                     'dinner' if 'dinner' in x.lower() else 'snack')

        # Features to use for recommendation
        self.features = [
            'calories', 'protein', 'fat', 'carbs', 'prep_time',
            'vegan', 'vegetarian', 'keto'
        ]

        return self.meal_data

    def train_model(self):
        """Train the recommendation model"""
        if self.meal_data is None:
            self.load_data()

        # Preprocessing pipeline
        numeric_features = ['calories', 'protein', 'fat', 'carbs', 'prep_time']
        binary_features = ['vegan', 'vegetarian', 'keto']

        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        binary_transformer = 'passthrough'

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('bin', binary_transformer, binary_features)
            ])

        # Prepare features
        X = self.meal_data[self.features]
        X_processed = self.preprocessor.fit_transform(X)

        # Train KNN model
        self.model = NearestNeighbors(n_neighbors=50, algorithm='auto', metric='cosine')
        self.model.fit(X_processed)

        return self.model

    def save_model(self, model_path='meal_recommender.joblib'):
        """Save the trained model and preprocessor"""
        if not os.path.exists(model_path):
            joblib.dump({
                'model': self.model,
                'preprocessor': self.preprocessor,
                'meal_data': self.meal_data,
                'features': self.features
            }, model_path)

    def load_saved_model(self, model_path='meal_recommender.joblib'):
        """Load a previously saved model"""
        saved_data = joblib.load(model_path)
        self.model = saved_data['model']
        self.preprocessor = saved_data['preprocessor']
        self.meal_data = saved_data['meal_data']
        self.features = saved_data['features']
        return self.model

    def recommend_meals(self, user_preferences, n_recommendations=3):
        """
        Recommend meals based on user preferences

        Args:
            user_preferences (dict): Dictionary containing user's preferences including:
                - calories (int)
                - protein (int, optional)
                - fat (int, optional)
                - carbs (int, optional)
                - prep_time (int, optional)
                - dietary_preference (str): 'none', 'vegan', 'vegetarian', 'keto'
                - meal_type (str): 'breakfast', 'lunch', 'dinner', 'snack'
            n_recommendations (int): Number of recommendations to return

        Returns:
            list: List of recommended meal dictionaries
        """
        if self.model is None:
            self.load_saved_model()  # Try to load saved model or train new one

        # Prepare query based on user preferences
        query = {
            'calories': user_preferences.get('calories', 500),
            'protein': user_preferences.get('protein', 20),
            'fat': user_preferences.get('fat', 15),
            'carbs': user_preferences.get('carbs', 60),
            'prep_time': user_preferences.get('prep_time', 20),
            'vegan': 1 if user_preferences.get('dietary_preference') == 'vegan' else 0,
            'vegetarian': 1 if user_preferences.get('dietary_preference') in ['vegetarian', 'vegan'] else 0,
            'keto': 1 if user_preferences.get('dietary_preference') == 'keto' else 0
        }

        # Create DataFrame for the query
        query_df = pd.DataFrame([query])[self.features]
        query_processed = self.preprocessor.transform(query_df)

        # Find nearest neighbors
        distances, indices = self.model.kneighbors(query_processed, n_neighbors=50)

        # Filter by meal type if specified
        meal_type = user_preferences.get('meal_type')
        if meal_type:
            filtered_indices = []
            filtered_distances = []
            for i, idx in enumerate(indices[0]):
                if self.meal_data.iloc[idx]['meal_type'] == meal_type:
                    filtered_indices.append(idx)
                    filtered_distances.append(distances[0][i])
                    if len(filtered_indices) >= n_recommendations:
                        break

            if not filtered_indices:
                # Fallback to any meal type if no exact matches
                filtered_indices = indices[0][:n_recommendations]
                filtered_distances = distances[0][:n_recommendations]
        else:
            filtered_indices = indices[0][:n_recommendations]
            filtered_distances = distances[0][:n_recommendations]

        # Prepare recommendations
        recommendations = []
        for idx, dist in zip(filtered_indices, filtered_distances):
            meal = self.meal_data.iloc[idx]
            recommendations.append({
                'name': meal['meal_name'],
                'calories': float(meal['calories']),
                'protein': float(meal['protein']),
                'fat': float(meal['fat']),
                'carbs': float(meal['carbs']),
                'prep_time': float(meal['prep_time']),
                'vegan': bool(meal['vegan']),
                'vegetarian': bool(meal['vegetarian']),
                'keto': bool(meal['keto']),
                'ingredients': [],  # Placeholder - would come from another dataset
                'instructions': [],  # Placeholder - would come from another dataset
                'similarity_score': float(1 - dist)  # Convert distance to similarity
            })

        return recommendations

    def generate_meal_plan(self, daily_calories, dietary_preference='none', age=30,
                          gender='male', height=170, weight=70, weight_goal='maintain'):
        """
        Generate a complete meal plan for a day based on user parameters

        Args:
            daily_calories (int): Target daily calories
            dietary_preference (str): Dietary restriction
            age (int): User's age
            gender (str): User's gender
            height (int): User's height in cm
            weight (int): User's weight in kg
            weight_goal (str): 'lose', 'maintain', or 'gain' weight

        Returns:
            dict: Complete meal plan with breakfast, lunch, dinner, and snacks
        """
        # Calculate meal calorie distribution
        if weight_goal == 'lose':
            # Slightly more protein for weight loss
            breakfast_cals = daily_calories * 0.25
            lunch_cals = daily_calories * 0.35
            dinner_cals = daily_calories * 0.3
            snack_cals = daily_calories * 0.1
            protein_ratio = 0.35
        elif weight_goal == 'gain':
            # More carbs for weight gain
            breakfast_cals = daily_calories * 0.3
            lunch_cals = daily_calories * 0.35
            dinner_cals = daily_calories * 0.25
            snack_cals = daily_calories * 0.1
            protein_ratio = 0.3
        else:  # maintain
            breakfast_cals = daily_calories * 0.25
            lunch_cals = daily_calories * 0.35
            dinner_cals = daily_calories * 0.3
            snack_cals = daily_calories * 0.1
            protein_ratio = 0.3

        # Generate meals for each time of day
        breakfast = self.recommend_meals({
            'calories': breakfast_cals,
            'protein': breakfast_cals * protein_ratio / 4,  # 4 cal/g protein
            'carbs': breakfast_cals * 0.5 / 4,  # 50% carbs
            'fat': breakfast_cals * 0.2 / 9,  # 20% fat
            'prep_time': 15,
            'dietary_preference': dietary_preference,
            'meal_type': 'breakfast'
        }, n_recommendations=1)[0]

        lunch = self.recommend_meals({
            'calories': lunch_cals,
            'protein': lunch_cals * protein_ratio / 4,
            'carbs': lunch_cals * 0.4 / 4,  # 40% carbs
            'fat': lunch_cals * 0.3 / 9,  # 30% fat
            'prep_time': 20,
            'dietary_preference': dietary_preference,
            'meal_type': 'lunch'
        }, n_recommendations=1)[0]

        dinner = self.recommend_meals({
            'calories': dinner_cals,
            'protein': dinner_cals * protein_ratio / 4,
            'carbs': dinner_cals * 0.3 / 4,  # 30% carbs
            'fat': dinner_cals * 0.4 / 9,  # 40% fat
            'prep_time': 30,
            'dietary_preference': dietary_preference,
            'meal_type': 'dinner'
        }, n_recommendations=1)[0]

        snacks = self.recommend_meals({
            'calories': snack_cals,
            'protein': snack_cals * 0.2 / 4,
            'carbs': snack_cals * 0.6 / 4,
            'fat': snack_cals * 0.2 / 9,
            'prep_time': 5,
            'dietary_preference': dietary_preference,
            'meal_type': 'snack'
        }, n_recommendations=2)

        # Calculate nutritional summary
        total_protein = breakfast['protein'] + lunch['protein'] + dinner['protein'] + sum(s['protein'] for s in snacks)
        total_carbs = breakfast['carbs'] + lunch['carbs'] + dinner['carbs'] + sum(s['carbs'] for s in snacks)
        total_fats = breakfast['fat'] + lunch['fat'] + dinner['fat'] + sum(s['fat'] for s in snacks)

        meal_plan = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner,
            'snacks': snacks,
            'totalCalories': daily_calories,
            'nutritionalSummary': {
                'protein': f"{round(total_protein)}g",
                'carbs': f"{round(total_carbs)}g",
                'fats': f"{round(total_fats)}g"
            }
        }

        return meal_plan

# Example usage
if __name__ == "__main__":
    recommender = MealRecommender()

    # First time - load data and train model
    recommender.load_data()
    recommender.train_model()
    recommender.save_model()

    # Subsequent times - load saved model
    # recommender.load_saved_model()

    # Generate a meal plan
    meal_plan = recommender.generate_meal_plan(
        daily_calories=2000,
        dietary_preference='vegetarian',
        age=30,
        gender='male',
        height=175,
        weight=70,
        weight_goal='maintain'
    )

    print("Generated Meal Plan:")
    print(f"Breakfast: {meal_plan['breakfast']['name']} ({meal_plan['breakfast']['calories']} cal)")
    print(f"Lunch: {meal_plan['lunch']['name']} ({meal_plan['lunch']['calories']} cal)")
    print(f"Dinner: {meal_plan['dinner']['name']} ({meal_plan['dinner']['calories']} cal)")
    # print(f"Snacks: {[s['name'] for s in meal_plan['snacks']}")
    print(f"Nutritional Summary: {meal_plan['nutritionalSummary']} ")

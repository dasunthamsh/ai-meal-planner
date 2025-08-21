import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
import re
from config import DATA_PATH, SCALER_SAVE_PATH, COMMON_ALLERGENS

class DataPreprocessor:
    def __init__(self):
        self.df = None
        self.scaler = MinMaxScaler()
        self.vitamins = None
        self.diet_cols = None

    def load_data(self):
        self.df = pd.read_csv(DATA_PATH)
        return self.df

    def preprocess_data(self):
        # Convert boolean columns to integers
        self.diet_cols = ['vegan', 'vegetarian', 'keto', 'paleo', 'gluten_free', 'mediterranean']
        for col in self.diet_cols:
            self.df[col] = self.df[col].astype(int)

        # Process ingredients - convert to lowercase and split
        self.df['ingredients'] = self.df['ingredients'].str.lower()

        # One-hot encode vitamins
        vitamins = set()
        for item in self.df['vitamins']:
            for vitamin in item.split(', '):
                vitamins.add(vitamin.strip())

        self.vitamins = list(vitamins)
        for vitamin in self.vitamins:
            self.df[vitamin] = self.df['vitamins'].apply(lambda x: 1 if vitamin in x else 0)

        # Create allergen columns based on ingredients
        for allergen, keywords in COMMON_ALLERGENS.items():
            pattern = '|'.join(keywords)
            self.df[allergen] = self.df['ingredients'].apply(
                lambda x: 1 if re.search(pattern, x) else 0
            )

        # Ensure all required health-related columns exist with default values if missing
        health_columns = ['sugar_g', 'added_sugar_g', 'sodium_mg', 'saturated_fat_g',
                          'fiber_g', 'cholesterol_mg', 'potassium_mg', 'omega3_g']

        for col in health_columns:
            if col not in self.df.columns:
                self.df[col] = 0  # Default value for missing health columns

        # Normalize numerical features (already per 100g)
        num_cols = ['calories', 'protein', 'fat', 'carbs'] + health_columns
        num_cols = [col for col in num_cols if col in self.df.columns]

        self.df[num_cols] = self.scaler.fit_transform(self.df[num_cols])

        # Save scaler for later use
        with open(SCALER_SAVE_PATH, 'wb') as f:
            pickle.dump(self.scaler, f)

        return self.df, self.scaler, self.vitamins, self.diet_cols

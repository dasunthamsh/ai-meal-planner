import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
import re
from config import DATA_PATH, SCALER_SAVE_PATH, COMMON_ALLERGENS, NUTRITION_COLS

class DataPreprocessor:
    def __init__(self):
        self.df = None
        self.scaler = MinMaxScaler()
        self.vitamins = None
        self.diet_cols = None

    def load_data(self):
        try:
            self.df = pd.read_csv(DATA_PATH)
            print(f"Successfully loaded data with {len(self.df)} rows")
            return self.df
        except FileNotFoundError:
            print(f"Error: Data file not found at {DATA_PATH}")
            raise
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def preprocess_data(self):
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Diet columns
        self.diet_cols = ['vegan', 'vegetarian', 'keto', 'paleo', 'gluten_free', 'mediterranean']
        for col in self.diet_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(int)
            else:
                print(f"Warning: Diet column '{col}' not found in dataset")
                self.df[col] = 0  # default safe

        # Ingredients
        if 'ingredients' in self.df.columns:
            self.df['ingredients'] = self.df['ingredients'].astype(str).str.lower()
        else:
            print("Warning: 'ingredients' column not found in dataset")

        # Vitamins one-hot (optional)
        if 'vitamins' in self.df.columns:
            vitamins = set()
            for item in self.df['vitamins']:
                if pd.notna(item):
                    for vitamin in str(item).split(', '):
                        vitamins.add(vitamin.strip())
            self.vitamins = list(vitamins)
            for vitamin in self.vitamins:
                self.df[vitamin] = self.df['vitamins'].apply(
                    lambda x: 1 if pd.notna(x) and vitamin in str(x) else 0
                )
        else:
            self.vitamins = []

        # Allergen columns
        if 'ingredients' in self.df.columns:
            for allergen, keywords in COMMON_ALLERGENS.items():
                pattern = '|'.join(keywords)
                self.df[allergen] = self.df['ingredients'].apply(
                    lambda x: 1 if re.search(pattern, str(x)) else 0
                )

        # Ensure health/nutrition columns
        for col in NUTRITION_COLS:
            if col not in self.df.columns:
                print(f"Warning: Column '{col}' not found, setting to 0")
                self.df[col] = 0.0

        # Fill missing
        self.df[NUTRITION_COLS] = self.df[NUTRITION_COLS].fillna(0)

        # Normalize
        self.df[NUTRITION_COLS] = self.scaler.fit_transform(self.df[NUTRITION_COLS])

        # Save scaler + column order
        with open(SCALER_SAVE_PATH, 'wb') as f:
            pickle.dump({'scaler': self.scaler, 'columns': NUTRITION_COLS}, f)
        print(f"Scaler saved to {SCALER_SAVE_PATH}")

        return self.df, self.scaler, self.vitamins, self.diet_cols

    def validate_data(self):
        required_columns = ['meal_name', 'calories', 'protein', 'fat', 'carbs', 'ingredients', 'image_url']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            print(f"Warning: Missing columns in dataset: {missing_columns}")
            return False
        print("Data validation passed")
        return True

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

        # Convert boolean columns to integers if they exist
        self.diet_cols = ['vegan', 'vegetarian', 'keto', 'paleo', 'gluten_free', 'mediterranean']
        for col in self.diet_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(int)
            else:
                print(f"Warning: Diet column '{col}' not found in dataset")

        # Process ingredients - convert to lowercase and ensure string type
        if 'ingredients' in self.df.columns:
            self.df['ingredients'] = self.df['ingredients'].astype(str).str.lower()
        else:
            print("Warning: 'ingredients' column not found in dataset")

        # One-hot encode vitamins if column exists
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
            print("Warning: 'vitamins' column not found in dataset")
            self.vitamins = []

        # Create allergen columns based on ingredients
        if 'ingredients' in self.df.columns:
            for allergen, keywords in COMMON_ALLERGENS.items():
                pattern = '|'.join(keywords)
                self.df[allergen] = self.df['ingredients'].apply(
                    lambda x: 1 if re.search(pattern, str(x)) else 0
                )
        else:
            print("Warning: Cannot create allergen columns - 'ingredients' column missing")

        # Ensure all required health-related columns exist with default values if missing
        health_columns = [
            'sugar_g', 'added_sugar_g', 'sodium_mg', 'saturated_fat_g',
            'fiber_g', 'cholesterol_mg', 'potassium_mg', 'omega3_g'
        ]

        for col in health_columns:
            if col not in self.df.columns:
                print(f"Warning: Health column '{col}' not found, setting default value 0")
                self.df[col] = 0

        # Ensure required nutrition columns exist
        required_nutrition_cols = ['calories', 'protein', 'fat', 'carbs']
        for col in required_nutrition_cols:
            if col not in self.df.columns:
                raise ValueError(f"Required nutrition column '{col}' not found in dataset")

        # Normalize numerical features (already per 100g)
        num_cols = required_nutrition_cols + health_columns
        num_cols = [col for col in num_cols if col in self.df.columns]

        print(f"Normalizing columns: {num_cols}")

        # Handle missing values before normalization
        for col in num_cols:
            if self.df[col].isnull().any():
                print(f"Warning: Column '{col}' has missing values, filling with 0")
                self.df[col] = self.df[col].fillna(0)

        self.df[num_cols] = self.scaler.fit_transform(self.df[num_cols])

        # Save scaler for later use
        try:
            with open(SCALER_SAVE_PATH, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"Scaler saved to {SCALER_SAVE_PATH}")
        except Exception as e:
            print(f"Error saving scaler: {e}")

        return self.df, self.scaler, self.vitamins, self.diet_cols

    def validate_data(self):
        """Validate that the dataset has all required columns"""
        required_columns = [
            'meal_name', 'calories', 'protein', 'fat', 'carbs',
            'ingredients', 'image_url'
        ]

        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            print(f"Warning: Missing columns in dataset: {missing_columns}")
            return False

        print("Data validation passed")
        return True

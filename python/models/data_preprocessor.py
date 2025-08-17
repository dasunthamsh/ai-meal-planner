import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
from config import DATA_PATH, SCALER_SAVE_PATH

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

        # One-hot encode vitamins
        vitamins = set()
        for item in self.df['vitamins']:
            for vitamin in item.split(', '):
                vitamins.add(vitamin.strip())

        self.vitamins = list(vitamins)
        for vitamin in self.vitamins:
            self.df[vitamin] = self.df['vitamins'].apply(lambda x: 1 if vitamin in x else 0)

        # Normalize numerical features
        num_cols = ['calories', 'protein', 'fat', 'carbs']
        self.df[num_cols] = self.scaler.fit_transform(self.df[num_cols])

        # Save scaler for later use
        with open(SCALER_SAVE_PATH, 'wb') as f:
            pickle.dump(self.scaler, f)

        return self.df, self.scaler, self.vitamins, self.diet_cols

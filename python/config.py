# Configuration constants
DATA_PATH = "dataset/meal_plan_dataset.csv"
MODEL_SAVE_PATH = "models/saved_agent.pkl"
SCALER_SAVE_PATH = "models/scaler.pkl"

# RL Hyperparameters
RL_ALPHA = 0.1  # Learning rate
RL_GAMMA = 0.6  # Discount factor
RL_EPSILON = 0.1  # Exploration rate

COMMON_ALLERGENS = {
    'dairy': ['milk', 'cheese', 'butter', 'cream', 'yogurt'],
    'eggs': ['egg', 'eggs'],
    'gluten': ['wheat', 'barley', 'rye', 'flour', 'bread', 'pasta'],
    'nuts': ['almond', 'cashew', 'peanut', 'walnut', 'pecan', 'hazelnut'],
    'soy': ['soy', 'tofu', 'soybean'],
    'fish': ['fish', 'salmon', 'tuna', 'cod'],
    'shellfish': ['shrimp', 'prawn', 'lobster', 'crab', 'clam']
}

# Health risk thresholds
HEALTH_RISK_THRESHOLDS = {
    'High blood pressure': {'sodium_mg': 500},
    'High cholesterol': {'cholesterol_mg': 100, 'saturated_fat_g': 5},
    'Diabetes': {'sugar_g': 10, 'added_sugar_g': 5},
    'Heart disease or stroke': {'saturated_fat_g': 5, 'cholesterol_mg': 100, 'sodium_mg': 500},
    'Testosterone deficiency': {'omega3_g': 0.5},
    'Depression': {'omega3_g': 0.5}
}

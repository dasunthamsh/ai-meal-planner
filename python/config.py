# Configuration constants
DATA_PATH = "dataset/meal_plan_dataset.csv"
MODEL_SAVE_PATH = "models/saved_genetic_algorithm.pkl"
SCALER_SAVE_PATH = "models/scaler.pkl"


# Genetic Algorithm Hyperparameters
GA_POPULATION_SIZE = 100
GA_GENERATIONS = 200
GA_MUTATION_RATE = 0.1
GA_CROSSOVER_RATE = 0.8
GA_ELITISM_COUNT = 5
GA_TOURNAMENT_SIZE = 5

# Fitness weights
FITNESS_WEIGHTS = {
    'calorie_match': 0.4,
    'protein_match': 0.3,
    'fat_match': 0.1,
    'carb_match': 0.1,
    'variety': 0.05,
    'health_restrictions': 0.05
}

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

# Diet type mappings
DIET_TYPE_MAPPING = {
    'No restrictions': 'none',
    'Vegetarian': 'vegetarian',
    'Vegan': 'vegan',
    'Keto': 'keto',
    'Paleo': 'paleo',
    'Gluten Free': 'gluten_free',
    'Mediterranean': 'mediterranean'
}

# Default nutrition targets (calories, protein, fat, carbs)
DEFAULT_NUTRITION_TARGETS = {
    'Lose Weight': {'protein_ratio': 0.35, 'fat_ratio': 0.25, 'carb_ratio': 0.40},
    'Build Muscle': {'protein_ratio': 0.40, 'fat_ratio': 0.20, 'carb_ratio': 0.40},
    'Gain Weight': {'protein_ratio': 0.25, 'fat_ratio': 0.25, 'carb_ratio': 0.50},
    'Maintain Weight': {'protein_ratio': 0.30, 'fat_ratio': 0.30, 'carb_ratio': 0.40}
}

# Meal types
MEAL_TYPES = ['breakfast', 'lunch', 'dinner']

# Default number of days for meal plan
DEFAULT_DAYS = 7

# Serving size in grams
DEFAULT_SERVING_SIZE = 100

# Nutrition carryover to next day (30%)
NUTRITION_CARRYOVER = 0.3

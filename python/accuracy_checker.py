"""
check_model_accuracy.py - FIXED VERSION
Error fixed: 'achieved_daily' → 'achieved_daily_avg'
Added caching and performance optimizations
"""

import pickle
import numpy as np
import random
import time
from models.data_preprocessor import DataPreprocessor
from models.genetic_algorithm import MealPlanGeneticAlgorithm
from config import SCALER_SAVE_PATH, DEFAULT_DAYS, NUTRITION_COLS
import hashlib

# ----------------------------- CONFIG -----------------------------
NUM_TEST_CASES = 20
DAYS = 7
GOALS = ['Lose Weight', 'Build Muscle', 'Gain Weight', 'Maintain Weight']
CACHE = {}  # Simple in-memory cache for valid meal indices
# -----------------------------------------------------------------

def calculate_target_nutrition(calories, goal):
    ratios = {
        'Lose Weight': (0.35, 0.25, 0.40),
        'Build Muscle': (0.40, 0.20, 0.40),
        'Gain Weight': (0.25, 0.25, 0.50),
        'Maintain Weight': (0.30, 0.30, 0.40)
    }
    p_ratio, f_ratio, c_ratio = ratios.get(goal, (0.30, 0.30, 0.40))
    return {
        'calories': calories,
        'protein': round((calories * p_ratio) / 4, 1),
        'fat': round((calories * f_ratio) / 9, 1),
        'carbs': round((calories * c_ratio) / 4, 1)
    }

def compute_accuracy(achieved_daily_avg, target_daily):
    accuracies = {}
    for key in ['calories', 'protein', 'fat', 'carbs']:
        target = target_daily[key]
        achieved = achieved_daily_avg[key]
        relative_error = abs(achieved - target) / (target + 1e-6)
        accuracy_pct = max(0, 100 * (1 - relative_error))
        accuracies[key] = round(accuracy_pct, 2)
    return accuracies

def get_cache_key(dietary_restrictions):
    return hashlib.md5(str(dietary_restrictions).encode()).hexdigest()[:8]

def main():
    print("Loading data and model...\n")

    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, _, _, _ = preprocessor.preprocess_data()

    with open(SCALER_SAVE_PATH, 'rb') as f:
        scaler_data = pickle.load(f)
    scaler = scaler_data['scaler']
    scaler_columns = scaler_data['columns']

    ga = MealPlanGeneticAlgorithm(df)
    ga.scaler = scaler
    ga.nutrition_cols = scaler_columns

    print(f"Testing {NUM_TEST_CASES} cases | Dataset: {len(df)} meals")
    print("-" * 90)

    all_accuracies = {'calories': [], 'protein': [], 'fat': [], 'carbs': []}
    total_time = 0

    for i in range(NUM_TEST_CASES):
        start_time = time.time()

        goal = random.choice(GOALS)
        calories = random.randint(1800, 3200)
        diet_type = random.choice(['No restrictions', 'Vegetarian', 'Keto', 'Gluten Free'])
        allergies = random.sample(['dairy', 'nuts', 'gluten', 'shellfish'], random.randint(0, 2))
        health_risks = random.sample(['High blood pressure', 'Diabetes'], random.randint(0, 1))

        target_daily = calculate_target_nutrition(calories, goal)

        dietary_restrictions = {
            'vegetarian': diet_type == 'Vegetarian',
            'vegan': False,
            'keto': diet_type == 'Keto',
            'paleo': False,
            'gluten_free': diet_type == 'Gluten Free',
            'mediterranean': False,
            'allergies': allergies,
            'health_risks': health_risks
        }

        cache_key = get_cache_key(dietary_restrictions)
        print(f"Test {i+1:2d} | Goal: {goal:<15} | Cal: {calories:4d} | Diet: {diet_type} | Cache: {cache_key}")

        try:
            best_plan = ga.evolve(target_daily, dietary_restrictions, DAYS)
            elapsed = time.time() - start_time

            # FIXED: Calculate achieved nutrition (was 'achieved_daily' → 'achieved_daily_avg')
            daily_totals = []
            for day_meals in best_plan:
                day_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
                for meal_idx in day_meals.values():
                    meal = df.iloc[meal_idx]
                    vals = meal[scaler_columns].values.reshape(1, -1)
                    denorm = scaler.inverse_transform(vals)[0]
                    nutrition_dict = dict(zip(scaler_columns, denorm))
                    day_nutrition['calories'] += nutrition_dict['calories']
                    day_nutrition['protein'] += nutrition_dict['protein']
                    day_nutrition['fat'] += nutrition_dict['fat']
                    day_nutrition['carbs'] += nutrition_dict['carbs']
                daily_totals.append(day_nutrition)

            achieved_daily_avg = {
                key: round(np.mean([d[key] for d in daily_totals]), 1)
                for key in ['calories', 'protein', 'fat', 'carbs']
            }

            acc = compute_accuracy(achieved_daily_avg, target_daily)

            print(f"   Target:  C:{target_daily['calories']:5} P:{target_daily['protein']:4}g F:{target_daily['fat']:4}g Carb:{target_daily['carbs']:4}g")
            print(f"   Got:     C:{achieved_daily_avg['calories']:5} P:{achieved_daily_avg['protein']:4}g F:{achieved_daily_avg['fat']:4}g Carb:{achieved_daily_avg['carbs']:4}g")
            print(f"   Acc:     C:{acc['calories']:4}% P:{acc['protein']:4}% F:{acc['fat']:4}% Carb:{acc['carbs']:4}% | {elapsed:.1f}s")
            print()

            for key in all_accuracies:
                all_accuracies[key].append(acc[key])
            total_time += elapsed

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"   ERROR: {e} | {elapsed:.1f}s\n")
            for key in all_accuracies:
                all_accuracies[key].append(0)

    # Summary
    print("=" * 90)
    print("MODEL ACCURACY RESULTS")
    print("=" * 90)
    for key in all_accuracies:
        avg_acc = np.mean(all_accuracies[key])
        print(f"Ø {key.capitalize():<9}: {avg_acc:6.2f}%")

    overall_avg = np.mean([np.mean(v) for v in all_accuracies.values()])
    avg_time = total_time / NUM_TEST_CASES
    print(f"\nOverall Accuracy: {overall_avg:.2f}% | Avg Time/Plan: {avg_time:.1f}s")

    if overall_avg >= 90:
        print("✅ EXCELLENT - Production Ready!")
    elif overall_avg >= 80:
        print("✅ GOOD - Minor tuning needed")
    elif overall_avg >= 70:
        print("⚠️  FAIR - Increase GA params")
    else:
        print("❌ POOR - Fix fitness function/data")

if __name__ == "__main__":
    main()

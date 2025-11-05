import numpy as np
import random
import pickle
from collections import defaultdict
from config import (
    GA_POPULATION_SIZE, GA_GENERATIONS, GA_MUTATION_RATE,
    GA_CROSSOVER_RATE, GA_ELITISM_COUNT, GA_TOURNAMENT_SIZE,
    FITNESS_WEIGHTS, COMMON_ALLERGENS, HEALTH_RISK_THRESHOLDS,
    MODEL_SAVE_PATH
)

class MealPlanGeneticAlgorithm:
    def __init__(self, meals_df):
        self.meals = meals_df
        self.population = []
        self.fitness_scores = []
        self.best_solution = None
        self.best_fitness = -float('inf')

        # Store max values for normalization
        self.nutrition_max = {
            'calories': meals_df['calories'].max() if 'calories' in meals_df.columns else 1.0,
            'protein': meals_df['protein'].max() if 'protein' in meals_df.columns else 1.0,
            'fat': meals_df['fat'].max() if 'fat' in meals_df.columns else 1.0,
            'carbs': meals_df['carbs'].max() if 'carbs' in meals_df.columns else 1.0
        }

    def initialize_population(self, days, dietary_restrictions):
        """Initialize population with valid meal plans"""
        valid_meal_indices = self._get_valid_meals(dietary_restrictions)

        if not valid_meal_indices:
            raise ValueError("No valid meals found for the given restrictions")

        self.population = []
        for _ in range(GA_POPULATION_SIZE):
            individual = []
            for day in range(days):
                daily_meals = {}
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    meal_idx = random.choice(valid_meal_indices)
                    daily_meals[meal_type] = meal_idx
                individual.append(daily_meals)
            self.population.append(individual)

    def _get_valid_meals(self, dietary_restrictions):
        """Get list of meal indices that meet all dietary restrictions"""
        try:
            valid_mask = np.ones(len(self.meals), dtype=bool)

            # Apply dietary restrictions
            for restriction, value in dietary_restrictions.items():
                if restriction in ['vegetarian', 'vegan', 'keto', 'paleo', 'gluten_free', 'mediterranean'] and value:
                    if restriction in self.meals.columns:
                        valid_mask &= (self.meals[restriction] == 1)
                    else:
                        print(f"Warning: Diet column '{restriction}' not found in dataset")

            # Apply allergy restrictions
            allergies = dietary_restrictions.get('allergies', [])
            for allergy in allergies:
                allergy = allergy.lower()
                if allergy in COMMON_ALLERGENS and allergy in self.meals.columns:
                    valid_mask &= (self.meals[allergy] == 0)

            # Apply health risk restrictions
            health_risks = dietary_restrictions.get('health_risks', [])
            for risk in health_risks:
                if risk == 'High blood pressure' and 'sodium_mg' in self.meals.columns:
                    valid_mask &= (self.meals['sodium_mg'] < 500)
                elif risk == 'High cholesterol' and 'cholesterol_mg' in self.meals.columns and 'saturated_fat_g' in self.meals.columns:
                    valid_mask &= (self.meals['cholesterol_mg'] < 100) & (self.meals['saturated_fat_g'] < 5)
                elif risk == 'Diabetes' and 'sugar_g' in self.meals.columns and 'added_sugar_g' in self.meals.columns:
                    valid_mask &= (self.meals['sugar_g'] < 10) & (self.meals['added_sugar_g'] < 5)
                elif risk == 'Heart disease or stroke':
                    if all(col in self.meals.columns for col in ['saturated_fat_g', 'cholesterol_mg', 'sodium_mg']):
                        valid_mask &= (self.meals['saturated_fat_g'] < 5) & (self.meals['cholesterol_mg'] < 100) & (self.meals['sodium_mg'] < 500)
                elif risk == 'Testosterone deficiency' and 'omega3_g' in self.meals.columns:
                    valid_mask &= (self.meals['omega3_g'] > 0.5)
                elif risk == 'Depression' and 'omega3_g' in self.meals.columns:
                    valid_mask &= (self.meals['omega3_g'] > 0.5)

            return [i for i, valid in enumerate(valid_mask) if valid]

        except Exception as e:
            print(f"Error in _get_valid_meals: {e}")
            return []

    def calculate_fitness(self, individual, target_nutrition, dietary_restrictions):
        """Calculate fitness score for an individual meal plan"""
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0
        meal_variety = set()
        health_penalty = 0

        serving_size = 100  # Standard serving size

        for day_meals in individual:
            for meal_type, meal_idx in day_meals.items():
                meal = self.meals.iloc[meal_idx]

                # Track meal variety
                meal_name = meal['meal_name'] if 'meal_name' in meal else f"meal_{meal_idx}"
                meal_variety.add(meal_name)

                # Add nutrition values
                total_calories += meal['calories'] * self.nutrition_max['calories'] * (serving_size / 100)
                total_protein += meal['protein'] * self.nutrition_max['protein'] * (serving_size / 100)
                total_fat += meal['fat'] * self.nutrition_max['fat'] * (serving_size / 100)
                total_carbs += meal['carbs'] * self.nutrition_max['carbs'] * (serving_size / 100)

                # Check health restrictions
                health_penalty += self._calculate_health_penalty(meal, dietary_restrictions.get('health_risks', []))

        # Calculate match scores (1 - normalized difference)
        days = len(individual)
        calorie_match = 1 - abs(total_calories - target_nutrition['calories'] * days) / (target_nutrition['calories'] * days + 1)
        protein_match = 1 - abs(total_protein - target_nutrition['protein'] * days) / (target_nutrition['protein'] * days + 1)
        fat_match = 1 - abs(total_fat - target_nutrition['fat'] * days) / (target_nutrition['fat'] * days + 1)
        carb_match = 1 - abs(total_carbs - target_nutrition['carbs'] * days) / (target_nutrition['carbs'] * days + 1)

        # Variety score (percentage of unique meals)
        variety_score = len(meal_variety) / (len(individual) * 3)  # 3 meals per day

        # Combine scores with weights
        fitness = (
                FITNESS_WEIGHTS['calorie_match'] * max(0, calorie_match) +
                FITNESS_WEIGHTS['protein_match'] * max(0, protein_match) +
                FITNESS_WEIGHTS['fat_match'] * max(0, fat_match) +
                FITNESS_WEIGHTS['carb_match'] * max(0, carb_match) +
                FITNESS_WEIGHTS['variety'] * variety_score +
                FITNESS_WEIGHTS['health_restrictions'] * (1 - health_penalty / (len(individual) * 3))
        )

        return fitness

    def _calculate_health_penalty(self, meal, health_risks):
        """Calculate penalty for violating health restrictions"""
        penalty = 0

        for risk in health_risks:
            if risk == 'High blood pressure' and 'sodium_mg' in meal:
                if meal['sodium_mg'] > 500:
                    penalty += 0.2
            elif risk == 'High cholesterol' and 'cholesterol_mg' in meal and 'saturated_fat_g' in meal:
                if meal['cholesterol_mg'] > 100 or meal['saturated_fat_g'] > 5:
                    penalty += 0.2
            elif risk == 'Diabetes' and 'sugar_g' in meal and 'added_sugar_g' in meal:
                if meal['sugar_g'] > 10 or meal['added_sugar_g'] > 5:
                    penalty += 0.2
            elif risk == 'Heart disease or stroke':
                if ('saturated_fat_g' in meal and meal['saturated_fat_g'] > 5 or
                        'cholesterol_mg' in meal and meal['cholesterol_mg'] > 100 or
                        'sodium_mg' in meal and meal['sodium_mg'] > 500):
                    penalty += 0.3
            elif risk == 'Testosterone deficiency' and 'omega3_g' in meal:
                if meal['omega3_g'] < 0.5:
                    penalty += 0.1
            elif risk == 'Depression' and 'omega3_g' in meal:
                if meal['omega3_g'] < 0.5:
                    penalty += 0.1

        return min(penalty, 1.0)  # Cap penalty at 1.0

    def tournament_selection(self):
        """Select parents using tournament selection"""
        selected = []
        for _ in range(2):  # Select 2 parents
            tournament = random.sample(list(zip(self.population, self.fitness_scores)), GA_TOURNAMENT_SIZE)
            winner = max(tournament, key=lambda x: x[1])[0]
            selected.append(winner)
        return selected

    def crossover(self, parent1, parent2):
        """Perform crossover between two parents"""
        if random.random() > GA_CROSSOVER_RATE:
            return parent1, parent2

        child1 = []
        child2 = []

        for day_idx in range(len(parent1)):
            if random.random() < 0.5:
                # Swap entire days
                child1.append(parent1[day_idx])
                child2.append(parent2[day_idx])
            else:
                # Swap individual meals
                child1_day = {}
                child2_day = {}
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    if random.random() < 0.5:
                        child1_day[meal_type] = parent1[day_idx][meal_type]
                        child2_day[meal_type] = parent2[day_idx][meal_type]
                    else:
                        child1_day[meal_type] = parent2[day_idx][meal_type]
                        child2_day[meal_type] = parent1[day_idx][meal_type]
                child1.append(child1_day)
                child2.append(child2_day)

        return child1, child2

    def mutate(self, individual, dietary_restrictions):
        """Mutate an individual by changing random meals"""
        valid_meal_indices = self._get_valid_meals(dietary_restrictions)

        for day_idx in range(len(individual)):
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                if random.random() < GA_MUTATION_RATE:
                    individual[day_idx][meal_type] = random.choice(valid_meal_indices)

        return individual

    def evolve(self, target_nutrition, dietary_restrictions, days=7):
        """Run the genetic algorithm evolution"""
        self.initialize_population(days, dietary_restrictions)

        for generation in range(GA_GENERATIONS):
            # Calculate fitness for all individuals
            self.fitness_scores = [
                self.calculate_fitness(ind, target_nutrition, dietary_restrictions)
                for ind in self.population
            ]

            # Track best solution
            best_idx = np.argmax(self.fitness_scores)
            if self.fitness_scores[best_idx] > self.best_fitness:
                self.best_fitness = self.fitness_scores[best_idx]
                self.best_solution = self.population[best_idx]

            # Create new population
            new_population = []

            # Elitism: keep best individuals
            elite_indices = np.argsort(self.fitness_scores)[-GA_ELITISM_COUNT:]
            for idx in elite_indices:
                new_population.append(self.population[idx])

            # Fill rest of population with crossover and mutation
            while len(new_population) < GA_POPULATION_SIZE:
                parent1, parent2 = self.tournament_selection()
                child1, child2 = self.crossover(parent1, parent2)

                child1 = self.mutate(child1, dietary_restrictions)
                child2 = self.mutate(child2, dietary_restrictions)

                new_population.extend([child1, child2])

            self.population = new_population[:GA_POPULATION_SIZE]

            if generation % 50 == 0:
                print(f"Generation {generation}, Best Fitness: {self.best_fitness:.4f}")

        return self.best_solution

    def save_model(self):
        """Save the trained model"""
        try:
            with open(MODEL_SAVE_PATH, 'wb') as f:
                pickle.dump({
                    'best_solution': self.best_solution,
                    'best_fitness': self.best_fitness,
                    'nutrition_max': self.nutrition_max
                }, f)
            print(f"Model saved successfully to {MODEL_SAVE_PATH}")
        except Exception as e:
            print(f"Error saving model: {e}")

    def load_model(self):
        """Load a trained model"""
        try:
            with open(MODEL_SAVE_PATH, 'rb') as f:
                data = pickle.load(f)
                self.best_solution = data['best_solution']
                self.best_fitness = data['best_fitness']
                self.nutrition_max = data['nutrition_max']
            print(f"Model loaded successfully from {MODEL_SAVE_PATH}")
            return True
        except FileNotFoundError:
            print("No saved model found")
            return False

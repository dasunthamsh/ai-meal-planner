import numpy as np
import random
import pickle
import copy
from config import (
    GA_POPULATION_SIZE, GA_GENERATIONS, GA_MUTATION_RATE,
    GA_CROSSOVER_RATE, GA_ELITISM_COUNT, GA_TOURNAMENT_SIZE,
    FITNESS_WEIGHTS, COMMON_ALLERGENS, MODEL_SAVE_PATH,
    HEALTH_RISK_THRESHOLDS, NUTRITION_COLS
)
from sklearn.preprocessing import MinMaxScaler

class MealPlanGeneticAlgorithm:
    def __init__(self, meals_df):
        self.meals = meals_df.reset_index(drop=True)
        self.scaler = MinMaxScaler()  # placeholder
        self.nutrition_cols = NUTRITION_COLS
        self.population = []
        self.fitness_scores = []
        self.best_solution = None
        self.best_fitness = -float('inf')

    def _denormalize_row(self, row):
        vals = row[self.nutrition_cols].values.reshape(1, -1)
        denorm = self.scaler.inverse_transform(vals)
        return dict(zip(self.nutrition_cols, denorm[0]))

    def _get_valid_meals(self, dietary_restrictions):
        df = self.meals
        valid_mask = np.ones(len(df), dtype=bool)

        for diet in ['vegetarian', 'vegan', 'keto', 'paleo', 'gluten_free', 'mediterranean']:
            if dietary_restrictions.get(diet, False) and diet in df.columns:
                valid_mask &= (df[diet] == 1)

        for allergy in dietary_restrictions.get('allergies', []):
            allergy = allergy.lower()
            if allergy in COMMON_ALLERGENS and allergy in df.columns:
                valid_mask &= (df[allergy] == 0)

        for risk in dietary_restrictions.get('health_risks', []):
            thresholds = HEALTH_RISK_THRESHOLDS.get(risk, {})
            for col, thresh in thresholds.items():
                if col in df.columns:
                    if 'omega3' in col:
                        valid_mask &= df.apply(lambda row: self._denormalize_row(row)[col] >= thresh, axis=1)
                    else:
                        valid_mask &= df.apply(lambda row: self._denormalize_row(row)[col] <= thresh, axis=1)

        return np.where(valid_mask)[0].tolist()

    def initialize_population(self, days, valid_meal_indices):
        self.population = []
        for _ in range(GA_POPULATION_SIZE):
            individual = []
            for _ in range(days):
                day_meals = {meal_type: random.choice(valid_meal_indices) for meal_type in ['breakfast', 'lunch', 'dinner']}
                individual.append(day_meals)
            self.population.append(individual)

    def calculate_fitness(self, individual, target_nutrition, days):
        total = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
        meal_names = set()

        for day_meals in individual:
            for meal_idx in day_meals.values():
                meal = self.meals.iloc[meal_idx]
                denorm = self._denormalize_row(meal)
                total['calories'] += denorm['calories']
                total['protein'] += denorm['protein']
                total['fat'] += denorm['fat']
                total['carbs'] += denorm['carbs']
                meal_names.add(meal['meal_name'])

        target_total = {k: v * days for k, v in target_nutrition.items()}

        matches = {}
        for key in ['calories', 'protein', 'fat', 'carbs']:
            diff = abs(total[key] - target_total[key])
            matches[key] = 1 - diff / (target_total[key] + 1e-6)

        variety_score = len(meal_names) / (days * 3)

        fitness = (
                FITNESS_WEIGHTS['calorie_match'] * max(0, matches['calories']) +
                FITNESS_WEIGHTS['protein_match'] * max(0, matches['protein']) +
                FITNESS_WEIGHTS['fat_match'] * max(0, matches['fat']) +
                FITNESS_WEIGHTS['carb_match'] * max(0, matches['carbs']) +
                FITNESS_WEIGHTS['variety'] * variety_score
        )
        return fitness

    def tournament_selection(self):
        tournament = random.sample(list(enumerate(self.fitness_scores)), GA_TOURNAMENT_SIZE)
        winner_idx = max(tournament, key=lambda x: x[1])[0]
        return self.population[winner_idx]

    def crossover(self, parent1, parent2):
        if random.random() > GA_CROSSOVER_RATE:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)  # return deep copies anyway
        child1, child2 = [], []
        for d1, d2 in zip(parent1, parent2):
            if random.random() < 0.5:
                child1.append(copy.deepcopy(d1))
                child2.append(copy.deepcopy(d2))
            else:
                child1.append(copy.deepcopy(d2))
                child2.append(copy.deepcopy(d1))
        return child1, child2

    # change random meals

    def mutate(self, individual, valid_meal_indices):
        mutated = copy.deepcopy(individual)
        for day in mutated:
            for meal_type in day:
                if random.random() < GA_MUTATION_RATE:
                    day[meal_type] = random.choice(valid_meal_indices)
        return mutated

    def evolve(self, target_nutrition, dietary_restrictions, days=7):
        valid_meal_indices = self._get_valid_meals(dietary_restrictions)
        if not valid_meal_indices:
            raise ValueError("No meals match the dietary restrictions.")

        self.initialize_population(days, valid_meal_indices)

        for generation in range(GA_GENERATIONS):
            self.fitness_scores = [
                self.calculate_fitness(ind, target_nutrition, days)
                for ind in self.population
            ]

            best_idx = np.argmax(self.fitness_scores)
            if self.fitness_scores[best_idx] > self.best_fitness:
                self.best_fitness = self.fitness_scores[best_idx]
                self.best_solution = copy.deepcopy(self.population[best_idx])  # <-- DEEP COPY

            # Elitism - deep copy elites
            elite_indices = np.argsort(self.fitness_scores)[-GA_ELITISM_COUNT:]
            new_population = [copy.deepcopy(self.population[i]) for i in elite_indices]
            # valid meal filter population initialz, best solution return
            while len(new_population) < GA_POPULATION_SIZE:
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, valid_meal_indices)
                child2 = self.mutate(child2, valid_meal_indices)
                new_population.extend([child1, child2])

            self.population = new_population[:GA_POPULATION_SIZE]

            if generation % 20 == 0:
                print(f"Gen {generation}, Best Fitness: {self.best_fitness:.4f}")

        return self.best_solution

    def save_model(self):
        with open(MODEL_SAVE_PATH, 'wb') as f:
            pickle.dump({
                'best_solution': self.best_solution,
                'best_fitness': self.best_fitness
            }, f)
        print("Model saved.")

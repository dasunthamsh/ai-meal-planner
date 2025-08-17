import random
import numpy as np
from collections import defaultdict
import pickle
from config import MODEL_SAVE_PATH, RL_ALPHA, RL_GAMMA, RL_EPSILON

class MealPlanRLAgent:
    def __init__(self, meals_df, alpha=RL_ALPHA, gamma=RL_GAMMA, epsilon=RL_EPSILON):
        self.meals = meals_df
        self.q_table = defaultdict(lambda: np.zeros(len(meals_df)))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.recent_meals = []

    def get_state_key(self, current_nutrition, remaining_days):
        return (
            round(current_nutrition['calories'], 1),
            round(current_nutrition['protein'], 1),
            round(current_nutrition['fat'], 1),
            round(current_nutrition['carbs'], 1),
            remaining_days
        )

    def choose_action(self, state, dietary_restrictions):
        valid_meal_indices = self._get_valid_meals(dietary_restrictions)

        if not valid_meal_indices:
            return None  # No valid meals found

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_meal_indices)
        else:
            q_values = self.q_table[state]
            valid_q_values = [q_values[i] for i in valid_meal_indices]
            max_q = max(valid_q_values)
            best_actions = [i for i in valid_meal_indices if q_values[i] == max_q]
            return random.choice(best_actions)

    def _get_valid_meals(self, dietary_restrictions):
        valid_mask = np.ones(len(self.meals), dtype=bool)

        # Apply dietary restrictions
        for restriction, value in dietary_restrictions.items():
            if restriction in self.meals.columns and value:
                valid_mask &= (self.meals[restriction] == 1)

        # Apply allergy restrictions
        allergies = dietary_restrictions.get('allergies', [])
        for allergy in allergies:
            if allergy.lower() in ['dairy', 'lactose']:
                valid_mask &= (self.meals['dairy'] == 0)
            elif allergy.lower() == 'eggs':
                valid_mask &= (self.meals['eggs'] == 0)

        return [i for i, valid in enumerate(valid_mask) if valid]

    def update_q_table(self, state, action, reward, next_state):
        if action is None:  # Skip if no valid action was found
            return

        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

    def calculate_reward(self, action, current_nutrition, target_nutrition, day):
        if action is None:
            return -1  # Penalty for no valid meal found

        meal = self.meals.iloc[action]

        # Calculate how much this meal helps reach targets
        calorie_diff = target_nutrition['calories'] - current_nutrition['calories']
        protein_diff = target_nutrition['protein'] - current_nutrition['protein']
        fat_diff = target_nutrition['fat'] - current_nutrition['fat']
        carb_diff = target_nutrition['carbs'] - current_nutrition['carbs']

        # Reward for moving toward targets
        calorie_reward = 1 - abs(calorie_diff - meal['calories']) / target_nutrition['calories']
        protein_reward = 1 - abs(protein_diff - meal['protein']) / target_nutrition['protein']
        fat_reward = 1 - abs(fat_diff - meal['fat']) / target_nutrition['fat']
        carb_reward = 1 - abs(carb_diff - meal['carbs']) / target_nutrition['carbs']

        # Variety reward
        variety_reward = 0.5 if meal['meal_name'] not in self.recent_meals[-3:] else -0.2

        # Combine rewards
        total_reward = (
                0.4 * calorie_reward +
                0.3 * protein_reward +
                0.1 * fat_reward +
                0.1 * carb_reward +
                0.1 * variety_reward
        )

        # Track recent meals
        self.recent_meals.append(meal['meal_name'])
        if len(self.recent_meals) > 5:
            self.recent_meals.pop(0)

        return total_reward

    def save_model(self):
        with open(MODEL_SAVE_PATH, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_model(self):
        try:
            with open(MODEL_SAVE_PATH, 'rb') as f:
                self.q_table = pickle.load(f)
            return True
        except FileNotFoundError:
            return False

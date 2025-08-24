import random
import numpy as np
from collections import defaultdict
import pickle
from config import MODEL_SAVE_PATH, RL_ALPHA, RL_GAMMA, RL_EPSILON, COMMON_ALLERGENS

class MealPlanRLAgent:
    def __init__(self, meals_df, alpha=RL_ALPHA, gamma=RL_GAMMA, epsilon=RL_EPSILON):
        self.meals = meals_df
        self.q_table = defaultdict(lambda: np.zeros(len(meals_df)))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.recent_meals = []

        # Store max values for normalization
        self.nutrition_max = {
            'calories': meals_df['calories'].max() if 'calories' in meals_df.columns else 1.0,
            'protein': meals_df['protein'].max() if 'protein' in meals_df.columns else 1.0,
            'fat': meals_df['fat'].max() if 'fat' in meals_df.columns else 1.0,
            'carbs': meals_df['carbs'].max() if 'carbs' in meals_df.columns else 1.0
        }

    def get_state_key(self, current_nutrition, remaining_days):
        """Create a state key from current nutrition and remaining days"""
        try:
            return (
                round(float(current_nutrition['calories']), 1),
                round(float(current_nutrition['protein']), 1),
                round(float(current_nutrition['fat']), 1),
                round(float(current_nutrition['carbs']), 1),
                int(remaining_days)
            )
        except (ValueError, TypeError) as e:
            print(f"Error creating state key: {e}")
            return (0.0, 0.0, 0.0, 0.0, remaining_days)

    def choose_action(self, state, dietary_restrictions):
        valid_meal_indices = self._get_valid_meals(dietary_restrictions)

        if not valid_meal_indices:
            return None

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_meal_indices)
        else:
            q_values = self.q_table[state]
            valid_q_values = [q_values[i] for i in valid_meal_indices]

            if not valid_q_values:
                return random.choice(valid_meal_indices)

            max_q = max(valid_q_values)
            best_actions = [i for i in valid_meal_indices if q_values[i] == max_q]
            return random.choice(best_actions) if best_actions else random.choice(valid_meal_indices)

    def find_alternative_meal(self, state, dietary_restrictions, excluded_action):
        """Find an alternative meal that meets all restrictions"""
        valid_meal_indices = self._get_valid_meals(dietary_restrictions)

        # Remove the excluded action
        valid_meal_indices = [i for i in valid_meal_indices if i != excluded_action]

        if not valid_meal_indices:
            return None

        # Get Q-values for valid meals
        q_values = self.q_table[state]
        valid_q_values = [q_values[i] for i in valid_meal_indices]

        if not valid_q_values:
            return random.choice(valid_meal_indices)

        max_q = max(valid_q_values)
        best_actions = [i for i in valid_meal_indices if q_values[i] == max_q]

        return random.choice(best_actions) if best_actions else random.choice(valid_meal_indices)

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

    def update_q_table(self, state, action, reward, next_state):
        if action is None:
            return

        try:
            best_next_action = np.argmax(self.q_table[next_state]) if next_state in self.q_table else 0
            td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
            td_error = td_target - self.q_table[state][action]
            self.q_table[state][action] += self.alpha * td_error
        except (KeyError, IndexError) as e:
            print(f"Error updating Q-table: {e}")

    def calculate_reward(self, action, current_nutrition, target_nutrition, day):
        if action is None:
            return -1

        try:
            meal = self.meals.iloc[action]

            # Calculate differences between current and target nutrition
            calorie_diff = target_nutrition['calories'] - current_nutrition['calories']
            protein_diff = target_nutrition['protein'] - current_nutrition['protein']
            fat_diff = target_nutrition['fat'] - current_nutrition['fat']
            carb_diff = target_nutrition['carbs'] - current_nutrition['carbs']

            # Calculate reward components
            calorie_reward = 1 - abs(calorie_diff - meal['calories']) / max(target_nutrition['calories'], 0.001)
            protein_reward = 1 - abs(protein_diff - meal['protein']) / max(target_nutrition['protein'], 0.001)
            fat_reward = 1 - abs(fat_diff - meal['fat']) / max(target_nutrition['fat'], 0.001)
            carb_reward = 1 - abs(carb_diff - meal['carbs']) / max(target_nutrition['carbs'], 0.001)

            # Variety reward to avoid repetitive meals
            meal_name = meal['meal_name'] if 'meal_name' in meal else f"meal_{action}"
            variety_reward = 0.5 if meal_name not in self.recent_meals[-3:] else -0.2

            # Weighted total reward
            total_reward = (
                    0.4 * calorie_reward +
                    0.3 * protein_reward +
                    0.1 * fat_reward +
                    0.1 * carb_reward +
                    0.1 * variety_reward
            )

            # Update recent meals list
            self.recent_meals.append(meal_name)
            if len(self.recent_meals) > 5:
                self.recent_meals.pop(0)

            return total_reward

        except Exception as e:
            print(f"Error calculating reward: {e}")
            return 0

    def save_model(self):
        try:
            # Convert defaultdict to regular dict for pickle
            q_table_dict = dict(self.q_table)
            with open(MODEL_SAVE_PATH, 'wb') as f:
                pickle.dump({
                    'q_table': q_table_dict,
                    'alpha': self.alpha,
                    'gamma': self.gamma,
                    'epsilon': self.epsilon
                }, f)
            print(f"Model saved successfully to {MODEL_SAVE_PATH}")
        except Exception as e:
            print(f"Error saving model: {e}")
            raise

    def load_model(self):
        try:
            with open(MODEL_SAVE_PATH, 'rb') as f:
                data = pickle.load(f)
                self.q_table = defaultdict(lambda: np.zeros(len(self.meals)), data['q_table'])
                self.alpha = data['alpha']
                self.gamma = data['gamma']
                self.epsilon = data['epsilon']
            print(f"Model loaded successfully from {MODEL_SAVE_PATH}")
            return True
        except (FileNotFoundError, KeyError, EOFError) as e:
            print(f"Error loading model: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error loading model: {e}")
            return False

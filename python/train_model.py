from models.meal_rl_agent import MealPlanRLAgent
from models.data_preprocessor import DataPreprocessor
import random
from config import MODEL_SAVE_PATH

def train_agent(agent, episodes=1000):
    print(f"Training RL agent for {episodes} episodes...")

    for episode in range(episodes):
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes}")

        # Random user parameters
        goal = random.choice(['Lose Weight', 'Build Muscle', 'Gain Weight', 'Maintain Weight'])
        diet_type = random.choice(['vegetarian', 'vegan', 'keto', 'paleo', 'gluten_free', 'mediterranean', 'none'])
        allergies = random.sample(['Dairy', 'Eggs', 'Gluten', 'Nuts'], random.randint(0, 2))

        dietary_restrictions = {
            'vegetarian': diet_type == 'vegetarian',
            'vegan': diet_type == 'vegan',
            'keto': diet_type == 'keto',
            'paleo': diet_type == 'paleo',
            'gluten_free': diet_type == 'gluten_free',
            'mediterranean': diet_type == 'mediterranean',
            'allergies': allergies
        }

        # Random calorie target
        calories = random.randint(1500, 3000)
        target_nutrition = {
            'calories': calories,
            'protein': calories * 0.3 / 4,  # 30% of calories from protein
            'fat': calories * 0.3 / 9,      # 30% of calories from fat
            'carbs': calories * 0.4 / 4     # 40% of calories from carbs
        }

        # Run simulation
        current_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
        days = 7

        for day in range(days):
            for _ in range(3):  # 3 meals per day
                state = agent.get_state_key(current_nutrition, days - day)
                action = agent.choose_action(state, dietary_restrictions)

                if action is None:
                    continue  # Skip if no valid meal found

                selected_meal = agent.meals.iloc[action]

                # Update nutrition
                current_nutrition['calories'] += selected_meal['calories']
                current_nutrition['protein'] += selected_meal['protein']
                current_nutrition['fat'] += selected_meal['fat']
                current_nutrition['carbs'] += selected_meal['carbs']

                # Update Q-table
                next_state = agent.get_state_key(current_nutrition, days - day - 1)
                reward = agent.calculate_reward(action, current_nutrition, target_nutrition, day)
                agent.update_q_table(state, action, reward, next_state)

            # Reset for next day (carry over some nutrition)
            current_nutrition = {k: v * 0.3 for k, v in current_nutrition.items()}

    # Save trained model
    agent.save_model()
    print("Training completed. Model saved to", MODEL_SAVE_PATH)

if __name__ == '__main__':
    # Initialize and preprocess data
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, scaler, vitamins, diet_cols = preprocessor.preprocess_data()

    # Initialize RL agent
    agent = MealPlanRLAgent(df)

    # Train the agent
    train_agent(agent, episodes=5000)

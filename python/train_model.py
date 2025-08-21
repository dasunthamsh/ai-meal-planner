from models.meal_rl_agent import MealPlanRLAgent
from models.data_preprocessor import DataPreprocessor
import random
from config import MODEL_SAVE_PATH, COMMON_ALLERGENS

def train_agent(agent, episodes=1000):
    print(f"Training RL agent for {episodes} episodes...")

    for episode in range(episodes):
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes}")

        goal = random.choice(['Lose Weight', 'Build Muscle', 'Gain Weight', 'Maintain Weight'])
        diet_type = random.choice(['vegetarian', 'vegan', 'keto', 'paleo', 'gluten_free', 'mediterranean', 'none'])
        allergies = random.sample(list(COMMON_ALLERGENS.keys()), random.randint(0, 2))
        health_risks = random.sample([
            'High blood pressure', 'High cholesterol', 'Diabetes',
            'Heart disease or stroke', 'Testosterone deficiency', 'Depression', 'None'
        ], random.randint(0, 2))

        if 'None' in health_risks:
            health_risks = []

        dietary_restrictions = {
            'vegetarian': diet_type == 'vegetarian',
            'vegan': diet_type == 'vegan',
            'keto': diet_type == 'keto',
            'paleo': diet_type == 'paleo',
            'gluten_free': diet_type == 'gluten_free',
            'mediterranean': diet_type == 'mediterranean',
            'allergies': allergies,
            'health_risks': health_risks
        }

        calories = random.randint(1500, 3000)
        target_nutrition = {
            'calories': calories,
            'protein': calories * 0.3 / 4,
            'fat': calories * 0.3 / 9,
            'carbs': calories * 0.4 / 4
        }

        current_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
        days = 7

        for day in range(days):
            for _ in range(3):
                state = agent.get_state_key({
                    'calories': current_nutrition['calories'] / agent.meals['calories'].max(),
                    'protein': current_nutrition['protein'] / agent.meals['protein'].max(),
                    'fat': current_nutrition['fat'] / agent.meals['fat'].max(),
                    'carbs': current_nutrition['carbs'] / agent.meals['carbs'].max()
                }, days - day)

                action = agent.choose_action(state, dietary_restrictions)

                if action is None:
                    continue

                selected_meal = agent.meals.iloc[action]

                current_nutrition['calories'] += selected_meal['calories'] * 100
                current_nutrition['protein'] += selected_meal['protein'] * 100
                current_nutrition['fat'] += selected_meal['fat'] * 100
                current_nutrition['carbs'] += selected_meal['carbs'] * 100

                next_state = agent.get_state_key({
                    'calories': current_nutrition['calories'] / agent.meals['calories'].max(),
                    'protein': current_nutrition['protein'] / agent.meals['protein'].max(),
                    'fat': current_nutrition['fat'] / agent.meals['fat'].max(),
                    'carbs': current_nutrition['carbs'] / agent.meals['carbs'].max()
                }, days - day - 1)

                reward = agent.calculate_reward(
                    action,
                    {
                        'calories': current_nutrition['calories'] / agent.meals['calories'].max(),
                        'protein': current_nutrition['protein'] / agent.meals['protein'].max(),
                        'fat': current_nutrition['fat'] / agent.meals['fat'].max(),
                        'carbs': current_nutrition['carbs'] / agent.meals['carbs'].max()
                    },
                    {
                        'calories': target_nutrition['calories'] / agent.meals['calories'].max(),
                        'protein': target_nutrition['protein'] / agent.meals['protein'].max(),
                        'fat': target_nutrition['fat'] / agent.meals['fat'].max(),
                        'carbs': target_nutrition['carbs'] / agent.meals['carbs'].max()
                    },
                    day
                )

                agent.update_q_table(state, action, reward, next_state)

            current_nutrition = {k: v * 0.3 for k, v in current_nutrition.items()}

    try:
        agent.save_model()
        print("Training completed. Model saved to", MODEL_SAVE_PATH)
    except Exception as e:
        print(f"Error saving model: {e}")
        print("Training completed but model could not be saved.")

if __name__ == '__main__':
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, scaler, vitamins, diet_cols = preprocessor.preprocess_data()

    agent = MealPlanRLAgent(df)

    train_agent(agent, episodes=5000)

from models.meal_rl_agent import MealPlanRLAgent
from models.data_preprocessor import DataPreprocessor
import matplotlib.pyplot as plt
import numpy as np

def plot_training_progress(episode_rewards):
    """Plot the reward progression during training"""
    plt.figure(figsize=(10, 5))

    # Simple moving average
    window_size = 50
    moving_avg = np.convolve(episode_rewards, np.ones(window_size)/window_size, mode='valid')

    plt.plot(episode_rewards, alpha=0.3, label='Episode Reward')
    plt.plot(moving_avg, label=f'{window_size}-episode Moving Avg')
    plt.xlabel('Episode')
    plt.ylabel('Average Reward')
    plt.title('Training Progress')
    plt.legend()
    plt.grid()
    plt.savefig('training_progress.png')
    plt.close()

def main():
    # Load data and model
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, _, _, _ = preprocessor.preprocess_data()

    agent = MealPlanRLAgent(df)

    if not agent.load_model():
        print("No trained model found. Please train the model first.")
        return

    # Evaluate the model
    results = agent.evaluate_performance(test_cases=100)

    print("\nModel Evaluation Results:")
    print(f"Average Reward: {results['average_reward']:.2f}")
    print(f"Goal Achievement Rate: {results['goal_achievement_rate']:.1f}%")

    # Sample meal plan generation for inspection
    print("\nSample Generated Meal Plan:")
    sample_plan = agent.generate_sample_plan()
    for day in sample_plan:
        print(f"\nDay {day['day']}:")
        for meal in day['meals']:
            for meal_type, details in meal.items():
                print(f"  {meal_type.capitalize()}: {details['meal_name']}")
                print(f"    Calories: {details['calories']:.0f}, Protein: {details['protein']:.1f}g")
        print(f"  Daily Total: {day['totalNutrition']['calories']:.0f} calories")

if __name__ == '__main__':
    main()

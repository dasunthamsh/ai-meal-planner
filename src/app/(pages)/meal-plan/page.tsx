"use client";

import { useState } from 'react';

type DietaryPreference = 'vegetarian' | 'vegan' | 'pescatarian' | 'gluten-free' | 'dairy-free' | 'none';

interface Meal {
    name: string;
    description: string;
    ingredients: string[];
    instructions: string[];
    calories: number;
    cookTime: number;
}

interface MealPlan {
    breakfast: Meal;
    lunch: Meal;
    dinner: Meal;
    snacks?: Meal[];
    totalCalories: number;
    nutritionalSummary: {
        protein: string;
        carbs: string;
        fats: string;
    };
}

export default function MealPlanner() {
    const [calories, setCalories] = useState<number>(2000);
    const [dietaryPreference, setDietaryPreference] = useState<DietaryPreference>('none');
    const [allergies, setAllergies] = useState<string>('');
    const [cuisine, setCuisine] = useState<string>('');
    const [cookingTime, setCookingTime] = useState<number>(30);
    const [generatedPlan, setGeneratedPlan] = useState<MealPlan | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const generateMealPlan = async () => {
        setIsLoading(true);

        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Generate mock data based on user inputs
        const mockPlan: MealPlan = {
            breakfast: {
                name: `${cuisine ? cuisine + ' ' : ''}${dietaryPreference !== 'none' ? dietaryPreference + ' ' : ''}Breakfast`,
                description: `A delicious ${dietaryPreference !== 'none' ? dietaryPreference + ' ' : ''}breakfast that's quick to prepare.`,
                ingredients: [
                    'Oats or whole grain bread',
                    'Fresh fruits',
                    'Nuts or seeds',
                    dietaryPreference === 'vegan' ? 'Plant-based milk' : 'Milk or yogurt',
                    'Honey or maple syrup'
                ],
                instructions: [
                    'Prepare your base (oats or toast)',
                    'Add fruits and toppings',
                    'Drizzle with sweetener if desired',
                    'Enjoy your nutritious breakfast'
                ],
                calories: Math.round(calories * 0.25),
                cookTime: 10
            },
            lunch: {
                name: `${cuisine ? cuisine + ' ' : ''}${dietaryPreference !== 'none' ? dietaryPreference + ' ' : ''}Lunch`,
                description: `A balanced ${dietaryPreference !== 'none' ? dietaryPreference + ' ' : ''}meal to keep you energized.`,
                ingredients: [
                    'Mixed greens or grain base',
                    'Protein source (tofu, chicken, fish, etc.)',
                    'Assorted vegetables',
                    'Healthy dressing',
                    'Whole grain bread or crackers'
                ],
                instructions: [
                    'Prepare your base (salad or grain)',
                    'Cook your protein if needed',
                    'Chop and add vegetables',
                    'Add dressing and toss',
                    'Serve with bread if desired'
                ],
                calories: Math.round(calories * 0.35),
                cookTime: cookingTime > 30 ? 20 : 15
            },
            dinner: {
                name: `${cuisine ? cuisine + ' ' : ''}${dietaryPreference !== 'none' ? dietaryPreference + ' ' : ''}Dinner`,
                description: `A satisfying ${dietaryPreference !== 'none' ? dietaryPreference + ' ' : ''}meal to end your day.`,
                ingredients: [
                    'Protein source',
                    'Complex carbohydrates',
                    'Seasonal vegetables',
                    'Healthy fats',
                    'Herbs and spices'
                ],
                instructions: [
                    'Prepare all ingredients',
                    'Cook protein to preference',
                    'Prepare sides',
                    'Plate and garnish',
                    'Enjoy your well-earned meal'
                ],
                calories: Math.round(calories * 0.4),
                cookTime: cookingTime
            },
            snacks: [
                {
                    name: 'Afternoon Snack',
                    description: 'A quick pick-me-up to keep you going.',
                    ingredients: [
                        'Fruits or vegetables',
                        'Nuts or seeds',
                        'Hummus or nut butter'
                    ],
                    instructions: [
                        'Wash and prepare fruits/veggies',
                        'Portion out nuts or dips',
                        'Enjoy mindfully'
                    ],
                    calories: 200,
                    cookTime: 5
                }
            ],
            totalCalories: calories,
            nutritionalSummary: {
                protein: `${Math.round(calories * 0.3 / 4)}g`,
                carbs: `${Math.round(calories * 0.4 / 4)}g`,
                fats: `${Math.round(calories * 0.3 / 9)}g`
            }
        };

        setGeneratedPlan(mockPlan);
        setIsLoading(false);
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-green-50 to-white py-12 px-4">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold text-green-700 mb-8 text-center">AI Meal Planner</h1>

                <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-8">
                    <div className="p-6 md:p-8">
                        <h2 className="text-2xl font-semibold text-green-700 mb-6">Your Preferences</h2>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Calories */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Daily Calorie Target
                                </label>
                                <input
                                    type="number"
                                    min="1000"
                                    max="5000"
                                    value={calories}
                                    onChange={(e) => setCalories(Number(e.target.value))}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>

                            {/* Dietary Preference */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Dietary Preference
                                </label>
                                <select
                                    value={dietaryPreference}
                                    onChange={(e) => setDietaryPreference(e.target.value as DietaryPreference)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                >
                                    <option value="none">No restrictions</option>
                                    <option value="vegetarian">Vegetarian</option>
                                    <option value="vegan">Vegan</option>
                                    <option value="pescatarian">Pescatarian</option>
                                    <option value="gluten-free">Gluten-free</option>
                                    <option value="dairy-free">Dairy-free</option>
                                </select>
                            </div>

                            {/* Allergies */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Allergies or Intolerances
                                </label>
                                <input
                                    type="text"
                                    value={allergies}
                                    onChange={(e) => setAllergies(e.target.value)}
                                    placeholder="e.g., peanuts, shellfish"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>

                            {/* Cuisine */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Preferred Cuisine
                                </label>
                                <input
                                    type="text"
                                    value={cuisine}
                                    onChange={(e) => setCuisine(e.target.value)}
                                    placeholder="e.g., Italian, Asian"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>

                            {/* Cooking Time */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Max Cooking Time (minutes)
                                </label>
                                <input
                                    type="number"
                                    min="10"
                                    max="120"
                                    value={cookingTime}
                                    onChange={(e) => setCookingTime(Number(e.target.value))}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>
                        </div>

                        <div className="mt-6">
                            <button
                                onClick={generateMealPlan}
                                disabled={isLoading}
                                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200 disabled:opacity-70"
                            >
                                {isLoading ? 'Generating...' : 'Generate Meal Plan'}
                            </button>
                        </div>
                    </div>
                </div>

                {generatedPlan && (
                    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                        <div className="p-6 md:p-8">
                            <h2 className="text-2xl font-semibold text-green-700 mb-6">Your Personalized Meal Plan</h2>

                            <div className="mb-8 p-4 bg-green-50 rounded-lg">
                                <h3 className="text-lg font-semibold text-green-800 mb-2">Nutritional Summary</h3>
                                <p className="text-gray-700"><span className="font-medium">Total Calories:</span> {generatedPlan.totalCalories}</p>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mt-2">
                                    <p className="text-gray-700"><span className="font-medium">Protein:</span> {generatedPlan.nutritionalSummary.protein}</p>
                                    <p className="text-gray-700"><span className="font-medium">Carbs:</span> {generatedPlan.nutritionalSummary.carbs}</p>
                                    <p className="text-gray-700"><span className="font-medium">Fats:</span> {generatedPlan.nutritionalSummary.fats}</p>
                                </div>
                            </div>

                            <div className="space-y-8">
                                {/* Breakfast */}
                                <div className="border border-gray-200 rounded-lg overflow-hidden">
                                    <div className="bg-green-100 px-4 py-3">
                                        <h3 className="text-lg font-semibold text-green-800">Breakfast: {generatedPlan.breakfast.name}</h3>
                                        <p className="text-sm text-gray-600">{generatedPlan.breakfast.calories} calories | {generatedPlan.breakfast.cookTime} min prep time</p>
                                    </div>
                                    <div className="p-4">
                                        <p className="text-gray-700 mb-3">{generatedPlan.breakfast.description}</p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <h4 className="font-medium text-gray-900 mb-2">Ingredients</h4>
                                                <ul className="list-disc pl-5 space-y-1 text-gray-700">
                                                    {generatedPlan.breakfast.ingredients.map((item, index) => (
                                                        <li key={index}>{item}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                            <div>
                                                <h4 className="font-medium text-gray-900 mb-2">Instructions</h4>
                                                <ol className="list-decimal pl-5 space-y-1 text-gray-700">
                                                    {generatedPlan.breakfast.instructions.map((step, index) => (
                                                        <li key={index}>{step}</li>
                                                    ))}
                                                </ol>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Lunch */}
                                <div className="border border-gray-200 rounded-lg overflow-hidden">
                                    <div className="bg-green-100 px-4 py-3">
                                        <h3 className="text-lg font-semibold text-green-800">Lunch: {generatedPlan.lunch.name}</h3>
                                        <p className="text-sm text-gray-600">{generatedPlan.lunch.calories} calories | {generatedPlan.lunch.cookTime} min prep time</p>
                                    </div>
                                    <div className="p-4">
                                        <p className="text-gray-700 mb-3">{generatedPlan.lunch.description}</p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <h4 className="font-medium text-gray-900 mb-2">Ingredients</h4>
                                                <ul className="list-disc pl-5 space-y-1 text-gray-700">
                                                    {generatedPlan.lunch.ingredients.map((item, index) => (
                                                        <li key={index}>{item}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                            <div>
                                                <h4 className="font-medium text-gray-900 mb-2">Instructions</h4>
                                                <ol className="list-decimal pl-5 space-y-1 text-gray-700">
                                                    {generatedPlan.lunch.instructions.map((step, index) => (
                                                        <li key={index}>{step}</li>
                                                    ))}
                                                </ol>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Dinner */}
                                <div className="border border-gray-200 rounded-lg overflow-hidden">
                                    <div className="bg-green-100 px-4 py-3">
                                        <h3 className="text-lg font-semibold text-green-800">Dinner: {generatedPlan.dinner.name}</h3>
                                        <p className="text-sm text-gray-600">{generatedPlan.dinner.calories} calories | {generatedPlan.dinner.cookTime} min prep time</p>
                                    </div>
                                    <div className="p-4">
                                        <p className="text-gray-700 mb-3">{generatedPlan.dinner.description}</p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <h4 className="font-medium text-gray-900 mb-2">Ingredients</h4>
                                                <ul className="list-disc pl-5 space-y-1 text-gray-700">
                                                    {generatedPlan.dinner.ingredients.map((item, index) => (
                                                        <li key={index}>{item}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                            <div>
                                                <h4 className="font-medium text-gray-900 mb-2">Instructions</h4>
                                                <ol className="list-decimal pl-5 space-y-1 text-gray-700">
                                                    {generatedPlan.dinner.instructions.map((step, index) => (
                                                        <li key={index}>{step}</li>
                                                    ))}
                                                </ol>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Snacks */}
                                {generatedPlan.snacks && generatedPlan.snacks.length > 0 && (
                                    <div className="border border-gray-200 rounded-lg overflow-hidden">
                                        <div className="bg-green-100 px-4 py-3">
                                            <h3 className="text-lg font-semibold text-green-800">Snacks</h3>
                                        </div>
                                        <div className="p-4 space-y-4">
                                            {generatedPlan.snacks.map((snack, index) => (
                                                <div key={index} className="border-b border-gray-100 pb-4 last:border-0 last:pb-0">
                                                    <h4 className="font-medium text-gray-900">{snack.name}</h4>
                                                    <p className="text-sm text-gray-600 mb-2">{snack.calories} calories | {snack.cookTime} min prep time</p>
                                                    <p className="text-gray-700 mb-2">{snack.description}</p>
                                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                        <div>
                                                            <h5 className="text-sm font-medium text-gray-900 mb-1">Ingredients</h5>
                                                            <ul className="list-disc pl-5 space-y-1 text-sm text-gray-700">
                                                                {snack.ingredients.map((item, idx) => (
                                                                    <li key={idx}>{item}</li>
                                                                ))}
                                                            </ul>
                                                        </div>
                                                        <div>
                                                            <h5 className="text-sm font-medium text-gray-900 mb-1">Instructions</h5>
                                                            <ol className="list-decimal pl-5 space-y-1 text-sm text-gray-700">
                                                                {snack.instructions.map((step, idx) => (
                                                                    <li key={idx}>{step}</li>
                                                                ))}
                                                            </ol>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

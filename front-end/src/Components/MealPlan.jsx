import { useState } from 'react';
import axios from 'axios';

const ComponentThree = ({ formData, onBack }) => {
    const [isGenerating, setIsGenerating] = useState(false);
    const [mealPlan, setMealPlan] = useState(null);
    const [error, setError] = useState(null);

    const generateMealPlan = async () => {
        setIsGenerating(true);
        setError(null);

        try {
            // Replace with your actual API endpoint
            const response = await axios.post('https://your-api-endpoint.com/generate-meal-plan', formData);
            setMealPlan(response.data);
        } catch (err) {
            setError('Failed to generate meal plan. Please try again.');
            console.error(err);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Summary & Meal Plan</h2>

            <div className="mb-8 bg-gray-50 p-6 rounded-lg">
                <h3 className="text-xl font-semibold text-gray-700 mb-4">Your Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <p className="text-gray-600"><span className="font-medium">Gender:</span> {formData.gender}</p>
                        <p className="text-gray-600"><span className="font-medium">Primary Goal:</span> {formData.goal}</p>
                        <p className="text-gray-600"><span className="font-medium">Current Body Fat:</span> {formData.currentBodyFat}%</p>
                        <p className="text-gray-600"><span className="font-medium">Goal Body Fat:</span> {formData.goalBodyFat}%</p>
                    </div>
                    <div>
                        <p className="text-gray-600"><span className="font-medium">Current Weight:</span> {formData.currentWeight} lbs</p>
                        <p className="text-gray-600"><span className="font-medium">Ideal Weight:</span> {formData.idealWeight} lbs</p>
                        <p className="text-gray-600"><span className="font-medium">Age:</span> {formData.age}</p>
                        <p className="text-gray-600"><span className="font-medium">Activity Level:</span> {formData.activityLevel}</p>
                    </div>
                </div>

                <div className="mt-6">
                    <h4 className="font-medium text-gray-700 mb-2">Dietary Preferences</h4>
                    <p className="text-gray-600"><span className="font-medium">Diet Type:</span> {formData.dietType}</p>
                    <p className="text-gray-600"><span className="font-medium">Allergies:</span> {formData.allergies.length > 0 ? formData.allergies.join(', ') : 'None'}</p>
                    <p className="text-gray-600"><span className="font-medium">Health Risks:</span> {formData.healthRisks.length > 0 ? formData.healthRisks.join(', ') : 'None'}</p>
                </div>

                <div className="mt-6 p-4 bg-blue-50 rounded-md">
                    <p className="text-blue-800 font-medium">
                        Recommended daily calories: <span className="font-bold">{formData.adjustedCalories} kcal</span>
                    </p>
                </div>
            </div>

            <div className="flex justify-between mb-8">
                <button
                    onClick={onBack}
                    className="px-6 py-2 bg-gray-200 text-gray-800 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
                >
                    Back
                </button>
                <button
                    onClick={generateMealPlan}
                    disabled={isGenerating}
                    className="px-6 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isGenerating ? 'Generating...' : 'Generate Meal Plan'}
                </button>
            </div>

            {error && (
                <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-md">
                    {error}
                </div>
            )}

            {mealPlan && (
                <div className="border-t pt-6">
                    <h3 className="text-xl font-semibold text-gray-700 mb-4">Your Personalized Meal Plan</h3>

                    <div className="space-y-6">
                        {mealPlan.days && mealPlan.days.map((day, index) => (
                            <div key={index} className="border rounded-lg overflow-hidden">
                                <div className="bg-gray-100 px-4 py-2 font-medium">
                                    Day {index + 1} - {day.totalCalories} kcal
                                </div>
                                <div className="p-4">
                                    <div className="mb-4">
                                        <h4 className="font-medium text-gray-700 mb-2">Breakfast</h4>
                                        <p>{day.breakfast.name} - {day.breakfast.calories} kcal</p>
                                        <p className="text-sm text-gray-600">Ingredients: {day.breakfast.ingredients.join(', ')}</p>
                                    </div>
                                    <div className="mb-4">
                                        <h4 className="font-medium text-gray-700 mb-2">Lunch</h4>
                                        <p>{day.lunch.name} - {day.lunch.calories} kcal</p>
                                        <p className="text-sm text-gray-600">Ingredients: {day.lunch.ingredients.join(', ')}</p>
                                    </div>
                                    <div>
                                        <h4 className="font-medium text-gray-700 mb-2">Dinner</h4>
                                        <p>{day.dinner.name} - {day.dinner.calories} kcal</p>
                                        <p className="text-sm text-gray-600">Ingredients: {day.dinner.ingredients.join(', ')}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-6 p-4 bg-green-50 rounded-md">
                        <h4 className="font-medium text-green-800 mb-2">Nutrition Summary</h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div>
                                <p className="text-sm text-green-700">Avg. Protein</p>
                                <p className="font-medium">{mealPlan.nutritionSummary.protein}g</p>
                            </div>
                            <div>
                                <p className="text-sm text-green-700">Avg. Carbs</p>
                                <p className="font-medium">{mealPlan.nutritionSummary.carbs}g</p>
                            </div>
                            <div>
                                <p className="text-sm text-green-700">Avg. Fat</p>
                                <p className="font-medium">{mealPlan.nutritionSummary.fat}g</p>
                            </div>
                            <div>
                                <p className="text-sm text-green-700">Avg. Fiber</p>
                                <p className="font-medium">{mealPlan.nutritionSummary.fiber}g</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ComponentThree;

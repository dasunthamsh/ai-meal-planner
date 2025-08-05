"use client";

import { useState } from 'react';

export default function MealPlanner() {
    const [calories, setCalories] = useState(2000);
    const [dietaryPreference, setDietaryPreference] = useState('none');
    const [age, setAge] = useState(30);
    const [gender, setGender] = useState('male');
    const [height, setHeight] = useState(170);
    const [weight, setWeight] = useState(70);
    const [weightGoal, setWeightGoal] = useState('maintain');
    const [generatedPlan, setGeneratedPlan] = useState(null);
    const [isLoading, setIsLoading] = useState(false);


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
                                    onChange={(e) => setDietaryPreference(e.target.value)}
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

                            {/* Age */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Age
                                </label>
                                <input
                                    type="number"
                                    min="1"
                                    max="120"
                                    value={age}
                                    onChange={(e) => setAge(Number(e.target.value))}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>

                            {/* Gender */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Gender
                                </label>
                                <select
                                    value={gender}
                                    onChange={(e) => setGender(e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                >
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            {/* Height */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Height (cm)
                                </label>
                                <input
                                    type="number"
                                    min="100"
                                    max="250"
                                    value={height}
                                    onChange={(e) => setHeight(Number(e.target.value))}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>

                            {/* Weight */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Weight (kg)
                                </label>
                                <input
                                    type="number"
                                    min="30"
                                    max="300"
                                    value={weight}
                                    onChange={(e) => setWeight(Number(e.target.value))}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                />
                            </div>

                            {/* Weight Goal */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Weight Goal
                                </label>
                                <select
                                    value={weightGoal}
                                    onChange={(e) => setWeightGoal(e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                >
                                    <option value="lose">Lose Weight</option>
                                    <option value="maintain">Maintain Weight</option>
                                    <option value="gain">Gain Weight</option>
                                </select>
                            </div>
                        </div>

                        <div className="mt-6">
                            <button

                                disabled={isLoading}
                                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200 disabled:opacity-70"
                            >
                                {isLoading ? 'Generating...' : 'Generate Meal Plan'}
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}

// Pages/SavedMealPlans.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Store } from 'react-notifications-component';

const SavedMealPlans = ({ loggedInUser }) => {
    const [mealPlans, setMealPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedPlan, setSelectedPlan] = useState(null);

    useEffect(() => {
        if (loggedInUser) {
            fetchSavedMealPlans();
        }
    }, [loggedInUser]);

    const fetchSavedMealPlans = async () => {
        try {
            const response = await axios.get(`http://localhost:3001/meal-plans/${loggedInUser}`);
            setMealPlans(response.data);
        } catch (err) {
            Store.addNotification({
                title: "Error!",
                message: "Failed to fetch saved meal plans",
                type: "danger",
                insert: "top",
                container: "top-right",
                dismiss: {
                    duration: 3000,
                    onScreen: true
                }
            });
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };
console.log(loggedInUser)
    const formatNumber = (num) => {
        return typeof num === 'number' ? num.toFixed(2) : num;
    };

    if (!loggedInUser) {
        return (
            <div className="min-h-screen bg-gray-100 py-8">
                <div className="max-w-4xl mx-auto px-4">
                    <div className="bg-white p-6 rounded-lg shadow-md text-center">
                        <h2 className="text-2xl font-bold text-gray-800 mb-4">Saved Meal Plans</h2>
                        <p className="text-gray-600">Please log in to view your saved meal plans.</p>
                    </div>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-100 py-8">
                <div className="max-w-4xl mx-auto px-4">
                    <div className="bg-white p-6 rounded-lg shadow-md text-center">
                        <h2 className="text-2xl font-bold text-gray-800 mb-4">Saved Meal Plans</h2>
                        <p className="text-gray-600">Loading your meal plans...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 py-8">
            <div className="max-w-6xl mx-auto px-4">
                <div className="bg-white p-6 rounded-lg shadow-md mb-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Saved Meal Plans</h2>
                    <p className="text-gray-600">Logged in as: {loggedInUser}</p>
                </div>

                {mealPlans.length === 0 ? (
                    <div className="bg-white p-6 rounded-lg shadow-md text-center">
                        <p className="text-gray-600">You haven't saved any meal plans yet.</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Meal Plan List */}
                        <div className="space-y-4">
                            <h3 className="text-xl font-semibold text-gray-700 mb-4">Select a Meal Plan</h3>
                            {mealPlans.map((plan, index) => (
                                <div
                                    key={index}
                                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                                        selectedPlan === plan
                                            ? 'bg-blue-50 border-blue-500'
                                            : 'bg-white border-gray-200 hover:bg-gray-50'
                                    }`}
                                    onClick={() => setSelectedPlan(plan)}
                                >
                                    <h4 className="font-medium text-gray-800">
                                        Meal Plan #{mealPlans.length - index}
                                    </h4>
                                    <p className="text-sm text-gray-600">
                                        Created: {formatDate(plan.createdAt)}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                        Goal: {plan.userData?.goal || 'N/A'}
                                    </p>
                                </div>
                            ))}
                        </div>

                        {/* Meal Plan Details */}
                        <div className="bg-white p-6 rounded-lg shadow-md">
                            <h3 className="text-xl font-semibold text-gray-700 mb-4">Meal Plan Details</h3>

                            {!selectedPlan ? (
                                <p className="text-gray-600">Select a meal plan to view details</p>
                            ) : (
                                <div>
                                    {/* User Information */}
                                    <div className="mb-6 bg-gray-50 p-4 rounded-md">
                                        <h4 className="font-medium text-gray-700 mb-2">User Information</h4>
                                        <div className="grid grid-cols-2 gap-2 text-sm">
                                            <p><span className="font-medium">Goal:</span> {selectedPlan.userData?.goal}</p>
                                            <p><span className="font-medium">Gender:</span> {selectedPlan.userData?.gender}</p>
                                            <p><span className="font-medium">Age:</span> {selectedPlan.userData?.age}</p>
                                            <p><span className="font-medium">Weight:</span> {selectedPlan.userData?.currentWeight} lbs</p>
                                        </div>
                                    </div>

                                    {/* Nutrition Summary */}
                                    {selectedPlan.nutritionSummary && (
                                        <div className="mb-6 bg-green-50 p-4 rounded-md">
                                            <h4 className="font-medium text-green-800 mb-2">Nutrition Summary</h4>
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                                <div>
                                                    <p className="text-green-700">Avg. Calories</p>
                                                    <p className="font-medium">{formatNumber(selectedPlan.nutritionSummary.avgCalories)} kcal</p>
                                                </div>
                                                <div>
                                                    <p className="text-green-700">Avg. Protein</p>
                                                    <p className="font-medium">{formatNumber(selectedPlan.nutritionSummary.avgProtein)}g</p>
                                                </div>
                                                <div>
                                                    <p className="text-green-700">Avg. Carbs</p>
                                                    <p className="font-medium">{formatNumber(selectedPlan.nutritionSummary.avgCarbs)}g</p>
                                                </div>
                                                <div>
                                                    <p className="text-green-700">Avg. Fat</p>
                                                    <p className="font-medium">{formatNumber(selectedPlan.nutritionSummary.avgFat)}g</p>
                                                </div>
                                            </div>
                                        </div>
                                    )}

                                    {/* Meal Plan Days */}
                                    {selectedPlan.planData && (
                                        <div>
                                            <h4 className="font-medium text-gray-700 mb-3">Meal Plan</h4>
                                            <div className="space-y-4 max-h-96 overflow-y-auto">
                                                {selectedPlan.planData.map((day) => (
                                                    <div key={day.day} className="border rounded-lg p-4">
                                                        <h5 className="font-medium text-blue-600 mb-2">Day {day.day}</h5>
                                                        <p className="text-sm text-gray-600 mb-2">
                                                            Total Calories: {formatNumber(day.totalNutrition?.calories)} kcal
                                                        </p>

                                                        {day.meals && day.meals.map((mealObj, mealIndex) => {
                                                            const mealType = Object.keys(mealObj)[0];
                                                            const meal = mealObj[mealType];
                                                            return (
                                                                <div key={mealIndex} className="flex justify-between mb-3 text-sm">
                                                                    <div>
                                                                        <p className="font-medium capitalize">{mealType}: {meal.meal_name}</p>
                                                                        <p className="text-gray-600">
                                                                            {formatNumber(meal.calories)} kcal |
                                                                            P: {formatNumber(meal.protein)}g |
                                                                            C: {formatNumber(meal.carbs)}g |
                                                                            F: {formatNumber(meal.fat)}g
                                                                        </p>
                                                                    </div>
                                                                    <div className='flex'>
                                                                        {meal.image_url && (
                                                                            <div className="mt-2 md:mt-0 md:ml-4">
                                                                                <img
                                                                                    src={meal.image_url}
                                                                                    alt={meal.meal_name}
                                                                                    className="w-16 h-16 object-cover rounded-md"
                                                                                />
                                                                            </div>
                                                                        )}
                                                                    </div>
                                                                </div>
                                                            );
                                                        })}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SavedMealPlans;

import { useState, useEffect } from 'react';
import workoutPlans from '../Data/workout-plans.json';
import { FaDumbbell, FaClock, FaFire, FaHeartbeat, FaLightbulb } from 'react-icons/fa';

const WorkoutPlan = ({ userData, onClose }) => {
    const [workoutPlan, setWorkoutPlan] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);

    useEffect(() => {
        generateWorkoutPlan();
    }, [userData]);

    const generateWorkoutPlan = () => {
        setIsGenerating(true);

        // Simulate API call delay
        setTimeout(() => {
            let selectedPlan;

            // Select workout plan based on user data
            if (userData.goal === 'Lose Weight') {
                selectedPlan = workoutPlans.workoutPlans.find(plan => plan.id === 2); // Weight Loss Circuit
            } else if (userData.goal === 'Gain Weight' || userData.goal === 'Build Muscle') {
                selectedPlan = workoutPlans.workoutPlans.find(plan => plan.id === 3); // Strength Building
            } else if (userData.activityLevel === 'Sedentary') {
                selectedPlan = workoutPlans.workoutPlans.find(plan => plan.id === 4); // Flexibility
            } else {
                selectedPlan = workoutPlans.workoutPlans.find(plan => plan.id === 1); // Beginner
            }

            // Adjust based on BMI
            if (userData.bmiCategory === 'Overweight' || userData.bmiCategory === 'Obese') {
                selectedPlan = workoutPlans.workoutPlans.find(plan => plan.id === 1); // Start with beginner
            }

            setWorkoutPlan(selectedPlan);
            setIsGenerating(false);
        }, 1500);
    };

    const handleRegenerate = () => {
        setIsGenerating(true);
        // Randomly select a different plan (for demo purposes)
        setTimeout(() => {
            const randomPlan = workoutPlans.workoutPlans[
                Math.floor(Math.random() * workoutPlans.workoutPlans.length)
                ];
            setWorkoutPlan(randomPlan);
            setIsGenerating(false);
        }, 1000);
    };

    if (isGenerating) {
        return (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white p-8 rounded-lg shadow-xl">
                    <div className="flex flex-col items-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                        <p className="text-lg font-medium text-gray-700">Generating your workout plan...</p>
                        <p className="text-gray-500 mt-2">Analyzing your goals and preferences</p>
                    </div>
                </div>
            </div>
        );
    }

    if (!workoutPlan) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-lg bg-white">
                {/* Header */}
                <div className="flex justify-between items-center mb-6">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800">Your Personalized Workout Plan</h2>
                        <p className="text-gray-600">Based on your goals and information</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="text-gray-500 hover:text-gray-700 text-2xl"
                    >
                        &times;
                    </button>
                </div>

                {/* Workout Plan Overview */}
                <div className="mb-8 p-6 bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
                        <div>
                            <h3 className="text-xl font-bold text-gray-800 mb-2">{workoutPlan.name}</h3>
                            <p className="text-gray-600 mb-4">{workoutPlan.description}</p>
                        </div>
                        <div className="flex space-x-4">
                            <div className="flex items-center">
                                <FaClock className="text-blue-500 mr-2" />
                                <span className="text-gray-700">{workoutPlan.duration}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* User Info Summary */}
                <div className="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-500">Goal</p>
                        <p className="font-medium">{userData.goal}</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-500">Activity Level</p>
                        <p className="font-medium">{userData.activityLevel}</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-500">BMI</p>
                        <p className="font-medium">{userData.bmi} ({userData.bmiCategory})</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-500">Recommended</p>
                        <p className="font-medium">Daily Workout</p>
                    </div>
                </div>

                {/* Exercises List */}
                <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                        <FaDumbbell className="mr-2 text-blue-500" />
                        Today's Exercises ({workoutPlan.exercises.length} exercises)
                    </h3>
                    <div className="space-y-4">
                        {workoutPlan.exercises.map((exercise, index) => (
                            <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                <div className="flex justify-between items-start">
                                    <div className="flex-1">
                                        <div className="flex items-center mb-2">
                                            <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mr-3">
                                                {index + 1}
                                            </div>
                                            <div>
                                                <h4 className="font-medium text-gray-800">{exercise.name}</h4>
                                                <p className="text-sm text-blue-600 font-medium">{exercise.sets}</p>
                                            </div>
                                        </div>
                                        <p className="text-gray-600 mb-2">{exercise.description}</p>
                                        <div className="flex items-center text-sm text-gray-500">
                                            <FaClock className="mr-1" size={12} />
                                            <span className="mr-4">Rest: {exercise.rest}</span>
                                        </div>
                                    </div>
                                    <div className="ml-4">
                                        <div className="w-24 h-24 bg-gray-200 rounded-lg flex items-center justify-center">
                                            {/* Replace with actual image */}
                                             <img src={`${exercise.image}`} alt={exercise.name} className="w-full h-full object-cover rounded-lg" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>





                {/* Action Buttons */}
                <div className="flex justify-between pt-6 border-t">
                    <button
                        onClick={handleRegenerate}
                        className="px-6 py-3 bg-gray-200 text-gray-800 font-medium rounded-lg hover:bg-gray-300 transition-colors flex items-center"
                    >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Generate Different Plan
                    </button>
                    <div className="space-x-3">
                        <button
                            onClick={onClose}
                            className="px-6 py-3 bg-gray-200 text-gray-800 font-medium rounded-lg hover:bg-gray-300 transition-colors"
                        >
                            Close
                        </button>
                        <button
                            onClick={() => window.print()}
                            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            Download Workout Plan
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default WorkoutPlan;

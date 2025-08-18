import { useState } from 'react';
import bodyImageOne from '../Assets/body0.png'
import bodyImageTwo from '../Assets/body 1.png'
import bodyImageThree from '../Assets/body2.png'
import bodyImageFour from '../Assets/body3.png'
import bodyImageFive from '../Assets/body4.png'
import bodyImageSix from '../Assets/body5.png'
const ComponentOne = ({ onNext }) => {
    const [formData, setFormData] = useState({
        gender: '',
        goal: '',
        currentBodyFat: '',
        goalBodyFat: '',
        currentWeight: '',
        idealWeight: '',
        age: '',
    });

    const [calories, setCalories] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const calculateCalories = () => {
        // Basic Harris-Benedict equation for calorie estimation
        const weightKg = parseFloat(formData.currentWeight) / 2.205;
        const age = parseInt(formData.age);

        let bmr;
        if (formData.gender === 'male') {
            bmr = 88.362 + (13.397 * weightKg) + (4.799 * 175) - (5.677 * age); // Assuming average height of 175cm
        } else {
            bmr = 447.593 + (9.247 * weightKg) + (3.098 * 162) - (4.330 * age); // Assuming average height of 162cm
        }

        // Adjust for goal
        let calorieAdjustment = 0;
        if (formData.goal === 'Lose Weight') calorieAdjustment = -500;
        else if (formData.goal === 'Gain Weight' || formData.goal === 'Build Muscle') calorieAdjustment = 500;

        const estimatedCalories = Math.round(bmr + calorieAdjustment);
        setCalories(estimatedCalories);
        return estimatedCalories;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const calculatedCalories = calculateCalories();
        onNext({ ...formData, calories: calculatedCalories });
    };

    const bodyFatOptions = [
        { value: '10-15', label: '10 - 15% (Ideal)', description: "You're in the elite! At this body fat %, you're leaner than 90% of men.", image:bodyImageTwo },
        { value: '15-20', label: '15 - 20% (Good)', description: "You have a healthy level of body fat and are leaner than 75% of men.", image:bodyImageThree },
        { value: '20-25', label: '20 - 25% (Ok)', description: "You have an average level of body fat which means you have a slightly higher risk of developing weight related health issues than a leaner version of yourself.", image:bodyImageFour },
        { value: '25-30', label: '25 - 30% (High)', description: "You have an above average level of body fat which elevates your risk of developing cardiovascular diseases, diabetes, and joint and mobility issues.", image:bodyImageFive},
        { value: '31-50', label: '31 - 50% (Very High)', description: "You have a very high level of body fat which elevates your risk of developing cardiovascular diseases, diabetes, and joint and mobility issues.", image:bodyImageSix },
    ];

    const goalBodyFatOptions = [
        { value: '6-10', label: '6 - 10% (Challenging)', description: "This is an ambitious goal but can definitely be achieved with enough time and effort.", image:bodyImageOne },
        { value: '10-15', label: '10 - 15% (Challenging)', description: "This is an ambitious goal but can definitely be achieved with enough time and effort.", image:bodyImageTwo },
        { value: '15-20', label: '15 - 20% (Challenging)', description: "This is an ambitious goal but can definitely be achieved with enough time and effort.", image:bodyImageThree },
        { value: '20-25', label: '20 - 25% (Realistic)', description: "Looks good! That's a realistic goal that can be achieved in a reasonable timeframe.", image:bodyImageFour },
        { value: '25-30', label: '25 - 30% (Realistic)', description: "Looks good! That's a realistic goal that can be achieved in a reasonable timeframe.", image:bodyImageFive },
        { value: '31-50', label: '31 - 50% (Current)', description: "Great! Health is more than just one variable, you don't need to lose fat to make progress. Your personalized plan will help you build muscle and get stronger and healthier.", image:bodyImageSix },
    ];

    return (
        <div className=" mx-auto p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Personal Information</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">1. What is your gender?</label>
                    <div className="flex space-x-4">
                        <label className="inline-flex items-center">
                            <input
                                type="radio"
                                name="gender"
                                value="male"
                                checked={formData.gender === 'male'}
                                onChange={handleChange}
                                className="form-radio h-5 w-5 text-blue-600"
                                required
                            />
                            <span className="ml-2">Male</span>
                        </label>
                        <label className="inline-flex items-center">
                            <input
                                type="radio"
                                name="gender"
                                value="female"
                                checked={formData.gender === 'female'}
                                onChange={handleChange}
                                className="form-radio h-5 w-5 text-blue-600"
                            />
                            <span className="ml-2">Female</span>
                        </label>
                    </div>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">2. What's your primary goal?</label>
                    <select
                        name="goal"
                        value={formData.goal}
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    >
                        <option value="">Select your goal</option>
                        <option value="Lose Weight">Lose Weight</option>
                        <option value="Maintain Weight">Maintain Weight</option>
                        <option value="Gain Weight">Gain Weight</option>
                        <option value="Build Muscle">Build Muscle</option>
                    </select>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">
                        3. Let's estimate your current body fat
                    </label>
                    <p className="text-gray-600 mb-3">Select the physique that most resembles your body type</p>
                    <div className="space-y-3">
                        {bodyFatOptions.map((option) => (
                            <div
                                key={option.value}
                                className="p-3 border border-gray-200 rounded-md hover:border-blue-400 flex items-start justify-between"
                            >
                                {/* Left side: Radio + Label + Description */}
                                <div>
                                    <label className="inline-flex items-center">
                                        <input
                                            type="radio"
                                            name="currentBodyFat"
                                            value={option.value}
                                            checked={formData.currentBodyFat === option.value}
                                            onChange={handleChange}
                                            className="form-radio h-5 w-5 text-blue-600"
                                            required
                                        />
                                        <span className="ml-2 font-medium">{option.label}</span>
                                    </label>
                                    <p className="ml-7 text-gray-600 text-sm">{option.description}</p>
                                </div>

                                {/* Right side: Image */}
                                <img
                                    src={option.image}
                                    alt={option.label}
                                    className="h-12 w-12 object-cover rounded-md"
                                />
                            </div>

                        ))}
                    </div>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">
                        4. Select your goal body fat/physique
                    </label>
                    <div className="space-y-3">
                        {goalBodyFatOptions.map((option) => (
                            <div
                                key={option.value}
                                className="p-3 border border-gray-200 rounded-md hover:border-blue-400 flex items-start justify-between"
                            >
                                {/* Left side: Radio + Label + Description */}
                                <div>
                                    <label className="inline-flex items-center">
                                        <input
                                            type="radio"
                                            name="goalBodyFat"
                                            value={option.value}
                                            checked={formData.goalBodyFat === option.value}
                                            onChange={handleChange}
                                            className="form-radio h-5 w-5 text-blue-600"
                                            required
                                        />
                                        <span className="ml-2 font-medium">{option.label}</span>
                                    </label>
                                    <p className="ml-7 text-gray-600 text-sm">{option.description}</p>
                                </div>

                                {/* Right side: Image */}
                                <img
                                    src={option.image}
                                    alt={option.label}
                                    className="h-12 w-12 object-cover rounded-md"
                                />
                            </div>
                        ))}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <label className="block text-gray-700 font-medium mb-2">5. What's your current weight?</label>
                        <div className="relative">
                            <input
                                type="number"
                                name="currentWeight"
                                value={formData.currentWeight}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="in pounds"
                                min="0"
                                required
                            />
                            <span className="absolute right-3 top-2 text-gray-500">lbs</span>
                        </div>
                    </div>
                    <div>
                        <label className="block text-gray-700 font-medium mb-2">6. What's your ideal weight?</label>
                        <div className="relative">
                            <input
                                type="number"
                                name="idealWeight"
                                value={formData.idealWeight}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="in pounds"
                                min="0"
                                required
                            />
                            <span className="absolute right-3 top-2 text-gray-500">lbs</span>
                        </div>
                    </div>
                </div>

                <div className="mb-8">
                    <label className="block text-gray-700 font-medium mb-2">7. How old are you?</label>
                    <input
                        type="number"
                        name="age"
                        value={formData.age}
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Age"
                        min="12"
                        max="120"
                        required
                    />
                </div>

                {calories && (
                    <div className="mb-6 p-4 bg-blue-50 rounded-md">
                        <p className="text-blue-800 font-medium">
                            Estimated daily calories: <span className="font-bold">{calories} kcal</span>
                        </p>
                    </div>
                )}

                <div className="flex justify-end">
                    <button
                        type="submit"
                        className="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                    >
                        Next
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ComponentOne;

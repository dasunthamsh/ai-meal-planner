import { useState, useEffect } from 'react';
import bodyImageOne from '../Assets/body0.png';
import bodyImageTwo from '../Assets/body 1.png';
import bodyImageThree from '../Assets/body2.png';
import bodyImageSix from '../Assets/body6.jpg';
import { FaMale, FaFemale } from 'react-icons/fa';

const ComponentOne = ({ onNext, initialData }) => {
    const [formData, setFormData] = useState(initialData || {
        gender: '',
        goal: '',
        currentWeight: '',
        age: '',
        height: ''
    });

    const [calories, setCalories] = useState(null);
    const [heightUnit, setHeightUnit] = useState('cm');
    const [bmi, setBmi] = useState(null);
    const [bmiCategory, setBmiCategory] = useState('');

    useEffect(() => {
        if (formData.currentWeight && formData.height && formData.height !== '0') {
            calculateBmi();
        }
    }, [formData.currentWeight, formData.height, heightUnit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleHeightUnitChange = (e) => {
        setHeightUnit(e.target.value);
    };

    const calculateBmi = () => {
        let heightM;
        if (heightUnit === 'cm') {
            heightM = parseFloat(formData.height) / 100;
        } else {
            // Convert feet to meters (1 foot = 0.3048 m)
            heightM = parseFloat(formData.height) * 0.3048;
        }

        const weightKg = parseFloat(formData.currentWeight);

        if (heightM > 0 && weightKg > 0) {
            const bmiValue = weightKg / (heightM * heightM);
            setBmi(bmiValue.toFixed(1));

            // Determine BMI category
            if (bmiValue < 18.5) {
                setBmiCategory('Underweight');
            } else if (bmiValue >= 18.5 && bmiValue < 25) {
                setBmiCategory('Healthy');
            } else if (bmiValue >= 25 && bmiValue < 30) {
                setBmiCategory('Overweight');
            } else {
                setBmiCategory('Obese');
            }
        }
    };

    const calculateCalories = () => {
        // Convert height to centimeters if needed
        let heightCm;
        if (heightUnit === 'cm') {
            heightCm = parseFloat(formData.height);
        } else {
            // Convert feet to centimeters (1 foot = 30.48 cm)
            heightCm = parseFloat(formData.height) * 30.48;
        }

        const weightKg = parseFloat(formData.currentWeight);
        const age = parseInt(formData.age);

        // Harris-Benedict equation with actual height
        let bmr;
        if (formData.gender === 'male') {
            bmr = 88.362 + (13.397 * weightKg) + (4.799 * heightCm) - (5.677 * age);
        } else {
            bmr = 447.593 + (9.247 * weightKg) + (3.098 * heightCm) - (4.330 * age);
        }

        const estimatedCalories = Math.round(bmr);
        setCalories(estimatedCalories);
        return estimatedCalories;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const calculatedCalories = calculateCalories();

        // Check for goal/BMI mismatch
        let showWarning = false;
        if ((bmiCategory === 'Overweight' || bmiCategory === 'Obese') && formData.goal === 'Gain Weight') {
            showWarning = true;
        } else if (bmiCategory === 'Underweight' && formData.goal === 'Lose Weight') {
            showWarning = true;
        }

        // Send data to parent component
        onNext({
            gender: formData.gender,
            goal: formData.goal,
            currentWeight: formData.currentWeight,
            age: formData.age,
            height: formData.height,
            heightUnit: heightUnit,
            calories: calculatedCalories,
            bmi: bmi,
            bmiCategory: bmiCategory,
            showWarning: showWarning
        });
    };

    const heightPlaceholder = heightUnit === 'cm' ? 'in centimeters' : 'in feet';

    // BMI Chart component
    const BmiChart = () => {
        return (
            <div className="mt-4 p-4 bg-gray-50 rounded-md">
                <h4 className="font-medium text-gray-700 mb-2">BMI Categories</h4>
                <div className="flex h-6 bg-gradient-to-r from-blue-400 via-green-400 via-yellow-400 to-red-500 rounded-full overflow-hidden">
                    <div className="w-1/5 text-xs text-center text-white flex items-center justify-center" style={{background: '#3b82f6'}}>Underweight</div>
                    <div className="w-1/5 text-xs text-center text-white flex items-center justify-center" style={{background: '#10b981'}}>Healthy</div>
                    <div className="w-1/5 text-xs text-center text-white flex items-center justify-center" style={{background: '#f59e0b'}}>Overweight</div>
                    <div className="w-2/5 text-xs text-center text-white flex items-center justify-center" style={{background: '#ef4444'}}>Obese</div>
                </div>
                <div className="flex justify-between text-xs mt-1">
                    <span>&lt;18.5</span>
                    <span>18.5-24.9</span>
                    <span>25-29.9</span>
                    <span>30+</span>
                </div>

                {bmi && (
                    <div className="mt-3">
                        <p className="text-sm">
                            Your BMI: <span className="font-bold">{bmi}</span> -
                            <span className={
                                bmiCategory === 'Underweight' ? 'text-blue-600 font-medium' :
                                    bmiCategory === 'Healthy' ? 'text-green-600 font-medium' :
                                        bmiCategory === 'Overweight' ? 'text-yellow-600 font-medium' :
                                            'text-red-600 font-medium'
                            }> {bmiCategory}</span>
                        </p>
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="mx-auto p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Personal Information</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-8">
                    <label className="block text-gray-700 font-medium mb-4 text-lg">1. What is your gender?</label>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <label className={`relative flex flex-col items-center p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                            formData.gender === 'male'
                                ? 'border-blue-500 bg-blue-50 shadow-md'
                                : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                        }`}>
                            <input
                                type="radio"
                                name="gender"
                                value="male"
                                checked={formData.gender === 'male'}
                                onChange={handleChange}
                                className="absolute opacity-0 h-0 w-0"
                                required
                            />
                            <div className={`p-3 rounded-full mb-3 ${
                                formData.gender === 'male' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'
                            }`}>
                                <FaMale size={24} />
                            </div>
                            <span className="font-medium text-gray-800">Male</span>
                            {formData.gender === 'male' && (
                                <div className="absolute top-2 right-2">
                                    <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                                        <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
                                    </div>
                                </div>
                            )}
                        </label>

                        <label className={`relative flex flex-col items-center p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                            formData.gender === 'female'
                                ? 'border-pink-500 bg-pink-50 shadow-md'
                                : 'border-gray-200 hover:border-pink-300 hover:bg-gray-50'
                        }`}>
                            <input
                                type="radio"
                                name="gender"
                                value="female"
                                checked={formData.gender === 'female'}
                                onChange={handleChange}
                                className="absolute opacity-0 h-0 w-0"
                            />
                            <div className={`p-3 rounded-full mb-3 ${
                                formData.gender === 'female' ? 'bg-pink-100 text-pink-600' : 'bg-gray-100 text-gray-600'
                            }`}>
                                <FaFemale size={24} />
                            </div>
                            <span className="font-medium text-gray-800">Female</span>
                            {formData.gender === 'female' && (
                                <div className="absolute top-2 right-2">
                                    <div className="w-4 h-4 bg-pink-500 rounded-full flex items-center justify-center">
                                        <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
                                    </div>
                                </div>
                            )}
                        </label>
                    </div>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">2. What's your primary goal?</label>
                    <p className="text-gray-600 mb-3">Select the goal that best matches your fitness objectives</p>
                    <div className="space-y-3">
                        {[
                            {
                                value: 'Lose Weight',
                                label: 'Lose Weight',
                                description: 'Focus on fat loss while maintaining muscle mass',
                                image: bodyImageTwo
                            },
                            {
                                value: 'Maintain Weight',
                                label: 'Maintain Weight',
                                description: 'Keep your current weight while improving fitness',
                                image: bodyImageSix
                            },
                            {
                                value: 'Gain Weight',
                                label: 'Gain Weight',
                                description: 'Increase overall body mass in a healthy way',
                                image: bodyImageThree
                            },
                            {
                                value: 'Build Muscle',
                                label: 'Build Muscle',
                                description: 'Focus on muscle growth and strength development',
                                image: bodyImageOne
                            }
                        ].map((option) => (
                            <label
                                key={option.value}
                                className={`flex items-start p-3 border rounded-md cursor-pointer transition-all duration-200 ${
                                    formData.goal === option.value
                                        ? 'border-blue-500 bg-blue-50 shadow-md'
                                        : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
                                }`}
                            >
                                <input
                                    type="radio"
                                    name="goal"
                                    value={option.value}
                                    checked={formData.goal === option.value}
                                    onChange={handleChange}
                                    className="mt-1 form-radio h-5 w-5 text-blue-600"
                                    required
                                />
                                <div className="ml-3 flex-1">
                                    <span className="font-medium text-gray-800">{option.label}</span>
                                    <p className="text-gray-600 text-sm">{option.description}</p>
                                </div>
                                <img
                                    src={option.image}
                                    alt={option.label}
                                    className="h-12 w-12 object-cover rounded-md ml-3"
                                />
                            </label>
                        ))}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <label className="block text-gray-700 font-medium mb-2">3. What's your current weight?</label>
                        <div className="relative">
                            <input
                                type="number"
                                name="currentWeight"
                                value={formData.currentWeight}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="in kilograms"
                                min="0"
                                step="0.1"
                                required
                            />
                            <span className="absolute right-3 top-2 text-gray-500">kg</span>
                        </div>
                    </div>
                    <div>
                        <label className="block text-gray-700 font-medium mb-2">4. How tall are you?</label>
                        <div className="flex items-center space-x-2">
                            <input
                                type="number"
                                name="height"
                                value={formData.height}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder={heightPlaceholder}
                                min="0"
                                step={heightUnit === 'cm' ? '1' : '0.1'}
                                required
                            />
                            <select
                                value={heightUnit}
                                onChange={handleHeightUnitChange}
                                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="cm">cm</option>
                                <option value="ft">ft</option>
                            </select>
                        </div>
                        <p className="text-sm text-gray-500 mt-1">
                            {heightUnit === 'cm'
                                ? 'Enter your height in centimeters'
                                : 'Enter your height in feet (e.g., 5.8 for 5 feet 8 inches)'}
                        </p>
                    </div>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">5. How old are you?</label>
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

                {/* BMI Calculation and Chart */}
                {bmi && <BmiChart />}

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

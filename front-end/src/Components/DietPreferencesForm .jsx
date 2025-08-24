import { useState } from 'react';

const ComponentTwo = ({ onNext, componentOneData }) => {
    const [formData, setFormData] = useState({
        activityLevel: '',
        dietType: 'No restrictions',
        allergies: [],
        healthRisks: [],
    });

    const [adjustedCalories, setAdjustedCalories] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleAllergyChange = (e) => {
        const { value, checked } = e.target;
        setFormData(prev => {
            if (checked) {
                return { ...prev, allergies: [...prev.allergies, value] };
            } else {
                return { ...prev, allergies: prev.allergies.filter(item => item !== value) };
            }
        });
    };

    const handleHealthRiskChange = (e) => {
        const { value, checked } = e.target;
        setFormData(prev => {
            if (checked) {
                return { ...prev, healthRisks: [...prev.healthRisks, value] };
            } else {
                return { ...prev, healthRisks: prev.healthRisks.filter(item => item !== value) };
            }
        });
    };

    const calculateAdjustedCalories = () => {
        const baseCalories = componentOneData.calories;
        let activityMultiplier = 1.0;

        switch(formData.activityLevel) {
            case 'Sedentary':
                activityMultiplier = 1.2;
                break;
            case 'Lightly active':
                activityMultiplier = 1.375;
                break;
            case 'Moderately active':
                activityMultiplier = 1.55;
                break;
            case 'Heavily active':
                activityMultiplier = 1.725;
                break;
            case 'Extremely active':
                activityMultiplier = 1.9;
                break;
            default:
                activityMultiplier = 1.2;
        }

        const adjusted = Math.round(baseCalories * activityMultiplier);
        setAdjustedCalories(adjusted);
        return adjusted;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const calculatedCalories = calculateAdjustedCalories();

        // Send only the required data to backend
        onNext({
            adjustedCalories: calculatedCalories,
            allergies: formData.allergies,
            dietType: formData.dietType,
            goal: componentOneData.goal,
            healthRisks: formData.healthRisks
        });
    };

    const activityOptions = [
        { value: 'Sedentary', label: 'Sedentary', description: 'Office worker, less than 30 minutes of light activity (cycling, brisk walking) per day' },
        { value: 'Lightly active', label: 'Lightly active', description: 'Office worker, 30+ minutes of light activity (cycling, brisk walking) per day' },
        { value: 'Moderately active', label: 'Moderately active', description: 'Teacher, salesman, 90+ minutes of light activity (cycling, brisk walking) per day' },
        { value: 'Heavily active', label: 'Heavily active', description: 'Janitor, waitress, 3+ hours of light activity (cycling, brisk walking) per day' },
        { value: 'Extremely active', label: 'Extremely active', description: 'Construction, landscaping, 4-5+ hours of light activity (cycling, brisk walking) per day' },
    ];

    const dietOptions = [
        'No restrictions',
        'Vegetarian',
        'Vegan',
        'Keto',
        'Paleo',
        'Gluten Free',
        'Mediterranean'
    ];

    const allergyOptions = [
        'Dairy (high lactose)',
        'All dairy',
        'Eggs',
        'Peanuts',
        'Tree nuts',
        'Soy',
        'Gluten',
        'Fish',
        'Shellfish'
    ];

    const healthRiskOptions = [
        'Testosterone deficiency',
        'Heart disease or stroke',
        'High blood pressure',
        'Diabetes',
        'High cholesterol',
        'Depression',
        'Other',
        'None'
    ];

    return (
        <div className=" mx-auto p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Activity & Preferences</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">1. How active are you?</label>
                    <div className="space-y-3">
                        {activityOptions.map((option) => (
                            <div key={option.value} className="p-3 border border-gray-200 rounded-md hover:border-blue-400">
                                <label className="inline-flex items-center">
                                    <input
                                        type="radio"
                                        name="activityLevel"
                                        value={option.value}
                                        checked={formData.activityLevel === option.value}
                                        onChange={handleChange}
                                        className="form-radio h-5 w-5 text-blue-600"
                                        required
                                    />
                                    <span className="ml-2 font-medium">{option.label}</span>
                                </label>
                                <p className="ml-7 text-gray-600 text-sm">{option.description}</p>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">2. Do you want to follow a special diet type?</label>
                    <select
                        name="dietType"
                        value={formData.dietType}
                        onChange={handleChange}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        {dietOptions.map(option => (
                            <option key={option} value={option}>{option}</option>
                        ))}
                    </select>
                </div>

                <div className="mb-6">
                    <label className="block text-gray-700 font-medium mb-2">3. Do you have any food allergies?</label>
                    <p className="text-gray-600 mb-3">Select all that apply</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {allergyOptions.map((option) => (
                            <label key={option} className="inline-flex items-center">
                                <input
                                    type="checkbox"
                                    value={option}
                                    checked={formData.allergies.includes(option)}
                                    onChange={handleAllergyChange}
                                    className="form-checkbox h-5 w-5 text-blue-600"
                                />
                                <span className="ml-2">{option}</span>
                            </label>
                        ))}
                    </div>
                </div>

                <div className="mb-8">
                    <label className="block text-gray-700 font-medium mb-2">4. Are you at risk of any of the following?</label>
                    <p className="text-gray-600 mb-3">Select all that apply</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {healthRiskOptions.map((option) => (
                            <label key={option} className="inline-flex items-center">
                                <input
                                    type="checkbox"
                                    value={option}
                                    checked={formData.healthRisks.includes(option)}
                                    onChange={handleHealthRiskChange}
                                    className="form-checkbox h-5 w-5 text-blue-600"
                                />
                                <span className="ml-2">{option}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {adjustedCalories && (
                    <div className="mb-6 p-4 bg-blue-50 rounded-md">
                        <p className="text-blue-800 font-medium">
                            Adjusted daily calories based on activity: <span className="font-bold">{adjustedCalories} kcal</span>
                        </p>
                    </div>
                )}

                <div className="flex justify-between">
                    <button
                        type="button"
                        onClick={() => window.scrollTo(0, 0)}
                        className="px-6 py-2 bg-gray-200 text-gray-800 font-medium rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
                    >
                        Back
                    </button>
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

export default ComponentTwo;

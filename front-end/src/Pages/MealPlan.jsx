import { useState } from 'react';
import ComponentOne from '../Components/BasicInfoForm';
import ComponentTwo from '../Components/DietPreferencesForm ';
import ComponentThree from '../Components/MealPlan';

const MealPlanGenerator = ({ loggedInUser }) => {
    const [currentStep, setCurrentStep] = useState(1);
    const [componentOneData, setComponentOneData] = useState(null);
    const [componentTwoData, setComponentTwoData] = useState(null);

    const handleComponentOneComplete = (data) => {
        setComponentOneData(data);
        setCurrentStep(2);
    };

    const handleComponentTwoComplete = (data) => {
        setComponentTwoData(data);
        setCurrentStep(3);
    };

    const handleBackFromComponentThree = () => {
        setCurrentStep(2);
    };

    const handleBackFromComponentTwo = () => {
        setCurrentStep(1);
    };

    return (
        <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-extrabold text-gray-900">Personalized Meal Plan Generator</h1>
                    <p className="mt-2 text-lg text-gray-600">Get a customized meal plan based on your goals and preferences</p>
                </div>

                <div className="mb-8">
                    <div className="flex items-center justify-between">
                        <div className={`flex-1 text-center ${currentStep >= 1 ? 'text-green-500' : 'text-gray-500'}`}>
                            <div className={`w-10 h-10 mx-auto rounded-full flex items-center justify-center ${currentStep >= 1 ? 'bg-green-500 text-white' : 'bg-gray-200'}`}>
                                1
                            </div>
                            <p className="mt-2 text-sm font-medium">Basic Info</p>
                        </div>
                        <div className={`flex-1 text-center ${currentStep >= 2 ? 'text-green-500' : 'text-gray-500'}`}>
                            <div className={`w-10 h-10 mx-auto rounded-full flex items-center justify-center ${currentStep >= 2 ? 'bg-green-500 text-white' : 'bg-gray-200'}`}>
                                2
                            </div>
                            <p className="mt-2 text-sm font-medium">Preferences</p>
                        </div>
                        <div className={`flex-1 text-center ${currentStep >= 3 ? 'text-green-500' : 'text-gray-500'}`}>
                            <div className={`w-10 h-10 mx-auto rounded-full flex items-center justify-center ${currentStep >= 3 ? 'bg-green-500 text-white' : 'bg-gray-200'}`}>
                                3
                            </div>
                            <p className="mt-2 text-sm font-medium">Meal Plan</p>
                        </div>
                    </div>

                </div>

                {currentStep === 1 && <ComponentOne onNext={handleComponentOneComplete} />}
                {currentStep === 2 && (
                    <ComponentTwo
                        onNext={handleComponentTwoComplete}
                        componentOneData={componentOneData}
                        onBack={handleBackFromComponentTwo}
                    />
                )}
                {currentStep === 3 && (
                    <ComponentThree
                        formData={componentTwoData}
                        onBack={handleBackFromComponentThree}
                        loggedInUser={loggedInUser}
                    />
                )}
            </div>
        </div>
    );
};

export default MealPlanGenerator;

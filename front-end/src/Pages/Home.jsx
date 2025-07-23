import React from 'react';
import { Link } from 'react-router-dom';
import Hero from "../Components/Hero";
import coverImage from "../Assets/foods.jpg"

function Home() {
    return (
        <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
            <head>
                <title>AI Meal Planner | Personalized Nutrition</title>
                <meta name="description" content="Generate personalized meal plans with AI" />
            </head>



            <main className="container mx-auto px-4 py-12">


                <div className='my-10'>
                    <Hero
                        coverImage={coverImage}
                        title="Welcome to AI Meal Planner"
                        subtitle="Personalized nutrition plans powered by artificial intelligence"
                    />
                </div>



                {/* Features Section */}
                <section className="max-w-6xl mx-auto mb-20">
                    <h2 className="text-3xl font-semibold text-center text-gray-800 mb-12">Why Choose Our Meal Planner</h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                            <div className="text-green-600 text-4xl mb-4">🍎</div>
                            <h3 className="text-xl font-medium text-gray-800 mb-2">Personalized Plans</h3>
                            <p className="text-gray-600">AI-generated meals tailored to your dietary needs and preferences.</p>
                        </div>

                        <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                            <div className="text-green-600 text-4xl mb-4">⏱️</div>
                            <h3 className="text-xl font-medium text-gray-800 mb-2">Save Time</h3>
                            <p className="text-gray-600">No more meal planning stress - we do the work for you.</p>
                        </div>

                        <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                            <div className="text-green-600 text-4xl mb-4">📊</div>
                            <h3 className="text-xl font-medium text-gray-800 mb-2">Nutrition Tracking</h3>
                            <p className="text-gray-600">Monitor your macros and micros with every meal plan.</p>
                        </div>
                    </div>
                </section>

                {/* How It Works Section */}
                <section className="max-w-4xl mx-auto mb-20 bg-white p-8 rounded-xl shadow-sm">
                    <h2 className="text-3xl font-semibold text-center text-gray-800 mb-8">How It Works</h2>

                    <div className="space-y-8">
                        <div className="flex flex-col md:flex-row items-center gap-6">
                            <div className="bg-green-100 text-green-800 rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl shrink-0">1</div>
                            <div>
                                <h3 className="text-xl font-medium text-gray-800 mb-2">Enter Your Preferences</h3>
                                <p className="text-gray-600">Tell us about your dietary needs, allergies, and food preferences.</p>
                            </div>
                        </div>

                        <div className="flex flex-col md:flex-row items-center gap-6">
                            <div className="bg-green-100 text-green-800 rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl shrink-0">2</div>
                            <div>
                                <h3 className="text-xl font-medium text-gray-800 mb-2">AI Generates Your Plan</h3>
                                <p className="text-gray-600">Our algorithm creates a perfectly balanced meal plan just for you.</p>
                            </div>
                        </div>

                        <div className="flex flex-col md:flex-row items-center gap-6">
                            <div className="bg-green-100 text-green-800 rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl shrink-0">3</div>
                            <div>
                                <h3 className="text-xl font-medium text-gray-800 mb-2">Enjoy Your Meals</h3>
                                <p className="text-gray-600">Cook delicious, nutritious meals with our easy-to-follow recipes.</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="text-center bg-green-800 text-white py-12 px-4 rounded-xl">
                    <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Eating Habits?</h2>
                    <p className="text-xl mb-8 max-w-2xl mx-auto">Join thousands of happy users who improved their nutrition with our AI Meal Planner.</p>
                    <button className="px-8 py-3 bg-white text-green-800 font-medium rounded-lg text-lg hover:bg-gray-100 transition-colors">
                        Start Your Free Trial
                    </button>
                </section>
            </main>

            <footer className="bg-green-900 text-white py-8">
                <div className="container mx-auto px-4">
                    <div className="flex flex-col md:flex-row justify-between items-center">
                        <div className="mb-4 md:mb-0">
                            <p className="text-xl font-bold">AI Meal Planner</p>
                            <p className="text-green-300">Personalized nutrition made easy</p>
                        </div>
                        <div className="flex space-x-6">
                            <a href="#" className="hover:text-green-300 transition-colors">About</a>
                            <a href="#" className="hover:text-green-300 transition-colors">Contact</a>
                            <a href="#" className="hover:text-green-300 transition-colors">Privacy</a>
                            <a href="#" className="hover:text-green-300 transition-colors">Terms</a>
                        </div>
                    </div>
                    <div className="mt-8 text-center text-green-300">
                        <p>© {new Date().getFullYear()} AI Meal Planner. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default Home;

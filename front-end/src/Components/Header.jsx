import React from 'react';
import { Link } from "react-router-dom";
import { FaHome, FaSignInAlt } from 'react-icons/fa';

const Header = () => {
    return (
        <header className="bg-white shadow hidden md:block relative">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                {/* Logo */}
                <div className="flex items-center space-x-4">
                    <span className="font-bold text-xl text-green-600">Meal-Planner</span>
                </div>

                {/* Navigation Links */}
                <nav className="flex space-x-6">
                    <Link to="/" className="flex items-center text-gray-600 hover:text-gray-900">
                        <FaHome className="" size={24} />
                    </Link>
                </nav>

                {/* Login Button */}
                <div className='flex'>
                    <Link to="/login" className="flex items-center text-gray-600 hover:text-gray-900 mx-2">
                        <FaSignInAlt className="mr-1" /> Login
                    </Link>
                </div>
            </div>
        </header>
    );
};

export default Header;

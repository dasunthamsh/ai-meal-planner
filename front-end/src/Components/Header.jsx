import React from 'react';
import { Link } from "react-router-dom";
import { FaHome, FaSignInAlt, FaHistory  } from 'react-icons/fa';
import { IoFastFood } from "react-icons/io5";


const Header = ({ loggedInUser }) => {
    return (
        <header className="bg-white shadow hidden md:block relative">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                {/* Logo */}
                <div className="flex items-center space-x-4">
                    <span className="font-bold text-xl text-green-600">Meal-Planner</span>
                    {loggedInUser ? (
                        <span className="text-gray-600">Welcome, {loggedInUser}</span>
                    ) : (
                    <></>
                    )}
                </div>

                {/* Navigation Links */}
                <nav className="flex space-x-6">
                    <Link to="/" className="flex items-center text-gray-600 hover:text-gray-900">
                        <FaHome className="" size={24} />
                    </Link>
                </nav>

                {/* Login Button */}
                <div className='flex'>

                    <Link to="/meals" className="flex items-center text-gray-600 hover:text-gray-900 mx-2">
                        <IoFastFood className="mr-1" /> Meals
                    </Link>

                    <Link to="/history" className="flex items-center text-gray-600 hover:text-gray-900 mx-2">
                        <FaHistory  className="mr-1" /> History
                    </Link>

                    <Link to="/login" className="flex items-center text-gray-600 hover:text-gray-900 mx-2">
                        <FaSignInAlt className="mr-1" /> Login
                    </Link>




                </div>

            </div>
        </header>
    );
};

export default Header;

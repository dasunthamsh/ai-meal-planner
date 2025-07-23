import React from 'react';
import {Link} from "react-router-dom";

const Hero = ({coverImage, title, subtitle}) => {


    return (
        <div>
            {/* Hero Section */}
            <div className="relative bg-gray-800 text-white rounded-lg overflow-hidden shadow-lg">
                <img
                    src={coverImage}
                    alt="Shoes Collection"
                    className="absolute inset-0 w-full h-full object-cover opacity-30"
                />
                <div className="relative p-10 md:p-20 lg:p-32 text-center">
                    <h1 className="text-4xl md:text-6xl font-bold">{title}</h1>
                    <p className="m-4 text-lg md:text-2xl">{subtitle}</p>
                    <Link to={"/meals"}>
                        <button className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg text-lg transition-colors">
                            Get Started
                        </button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Hero;




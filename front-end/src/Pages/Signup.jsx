import React, {useState} from 'react';
import axios from "axios";
import {Store} from "react-notifications-component";
import { useNavigate } from "react-router-dom";

const Signup = () => {

    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();
    const navigate = useNavigate();

    const handleSubmit =  (e) => {
        e.preventDefault();
        const formData = new FormData();
       formData.append('firstName', firstName);
       formData.append('lastName', lastName);
       formData.append('email', email);
       formData.append('password',  password);

       axios.post('http://localhost:3001/signup', formData, {
           headers: {
               'Content-Type':'multipart/form-data'
           }
       })
           .then(result => {
               Store.addNotification({
                   title: "Success!",
                   message: "Login successful!",
                   type: "success",
                   insert: "top",
                   container: "top-right",
                   dismiss: {
                       duration: 3000,
                       onScreen: true
                   }
               });
               navigate('/login')
           })
           .catch(error => {
               Store.addNotification({
                   title: "Error!",
                   message: `Login failed: ${error.response.data}`,
                   type: "danger",
                   insert: "top",
                   container: "top-right",
                   dismiss: {
                       duration: 3000,
                       onScreen: true
                   }
               });
           });
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-lg">
                <h2 className="text-2xl font-extrabold text-center text-gray-900">Create your account</h2>
                <form onSubmit={handleSubmit} className="mt-8 space-y-6">
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div>
                            <label htmlFor="first-name" className="sr-only">First Name</label>
                            <input
                                type="text"
                                value={firstName}
                                onChange={(e) => setFirstName(e.target.value)}
                                className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="First Name" />
                        </div>
                        <div>
                            <label htmlFor="last-name" className="sr-only">Last Name</label>
                            <input
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                type="text" autoComplete="family-name" required
                                className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Last Name" />
                        </div>
                        <div>
                            <label htmlFor="email-address" className="sr-only">Email address</label>
                            <input
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                type="email" autoComplete="email" required
                                className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Email address" />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">Password</label>
                            <input
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                type="password" autoComplete="current-password" required
                                className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password" />
                        </div>
                    </div>

                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <input id="terms" name="terms" type="checkbox" required className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500" />
                            <label htmlFor="terms" className="block ml-2 text-sm text-gray-900">
                                I agree to the <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">Terms and Conditions</a>
                            </label>
                        </div>
                    </div>

                    <div>
                        <button type="submit" className="relative flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md group hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Sign Up
                        </button>
                    </div>
                </form>
                <div className="mt-6 text-sm text-center text-gray-600">
                    Already have an account? <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">Sign In</a>
                </div>
            </div>
        </div>
    );
};

export default Signup;

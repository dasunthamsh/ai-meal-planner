import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import {Store} from "react-notifications-component";

const Login = ({ onLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();

        axios.post('http://localhost:3001/login', { email, password })
            .then(response => {
                onLogin(email);
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
            navigate('/')
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
                <h2 className="text-2xl font-extrabold text-center text-gray-900">Sign In</h2>
                <form onSubmit={handleSubmit} className="mt-8 space-y-6">
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div>
                            <label htmlFor="email-address" className="sr-only">Email address</label>
                            <input
                                id='email-address'
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Email address"
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">Password</label>
                            <input
                                id='password'
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                                placeholder="Password"
                            />
                        </div>
                    </div>

                    <div>
                        <button type="submit" className="relative flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md group hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Sign In
                        </button>
                    </div>
                </form>
                <div className="mt-6 text-sm text-center text-gray-600">
                    Don't have an account? <a href="/signup" className="font-medium text-indigo-600 hover:text-indigo-500">Sign Up</a>
                </div>
            </div>
        </div>
    );
};

export default Login;

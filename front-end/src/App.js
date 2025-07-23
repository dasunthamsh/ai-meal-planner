import './App.css';
import {BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Pages/Home"
import Header from "./Components/Header";
import Signup from "./Pages/Signup";
import Login from "./Pages/Login";
import { ReactNotifications } from 'react-notifications-component';
import 'react-notifications-component/dist/theme.css';
import {useState} from "react";
import MealPlanner from "./Pages/MealPlan";
function App() {

    const [loggedInUser, setLoggedInUser] = useState(null);
    const handleLogin = (email) => {
        setLoggedInUser(email);
    };

    return (
    <div>
        <ReactNotifications />
        <BrowserRouter>
            <Header/>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path='/meals' element={<MealPlanner />}></Route>
                <Route path="/signup" element={<Signup/>}></Route>
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
            </Routes>
      </BrowserRouter>

    </div>
  );
}
// constants.js

export default App;

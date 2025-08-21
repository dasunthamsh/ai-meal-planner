import './App.css';
import {BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Pages/Home"
import Header from "./Components/Header";
import Signup from "./Pages/Signup";
import Login from "./Pages/Login";
import History from "./Pages/SavedMealPlans";
import { ReactNotifications } from 'react-notifications-component';
import 'react-notifications-component/dist/theme.css';
import {useState} from "react";
import MealPlanner from "./Pages/MealPlan";
import SavedMealPlans from "./Pages/SavedMealPlans";
function App() {

    const [loggedInUser, setLoggedInUser] = useState(null);
    const handleLogin = (email) => {
        setLoggedInUser(email);
    };

    return (
    <div>
        <ReactNotifications />
        <BrowserRouter>
            <Header loggedInUser={loggedInUser}/>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path='/meals' element={<MealPlanner loggedInUser={loggedInUser} />}></Route>
                <Route path="/signup" element={<Signup/>}></Route>
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
                <Route path="/history" element={<SavedMealPlans loggedInUser={loggedInUser} />}></Route>

            </Routes>
      </BrowserRouter>

    </div>
  );
}
// constants.js

export default App;

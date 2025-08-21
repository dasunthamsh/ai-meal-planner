const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');
const UserModel = require('./models/User');
const path = require('path');
const app = express();
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

mongoose.connect("mongodb://localhost:27017/full-stack-db", { useNewUrlParser: true, useUnifiedTopology: true });

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});
const upload = multer({ storage: storage });

// Sign up user (add user)
app.post('/signup', upload.none(), (req, res) => {
    const { firstName, lastName, email, password  } = req.body;

    UserModel.create({ firstName, lastName, email, password  })
        .then(user => res.json(user))
        .catch(err => res.status(400).json(err));
});

// Login user
app.post('/login', upload.none(), async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await UserModel.findOne({ email });
        if (!user || user.password !== password) {
            return res.status(400).json({ message: 'Invalid email or password' });
        }

        res.json({ message: 'Login successful' });
    } catch (err) {
        res.status(500).json({ message: 'Something went wrong', error: err.message });
    }
});

// Save meal plan
app.post('/save-meal-plan', upload.none(), async (req, res) => {
    const { email, mealPlan, nutritionSummary, userData } = req.body;

    try {
        const user = await UserModel.findOne({ email });
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Add the new meal plan to the user's mealPlans array
        user.mealPlans.push({
            planData: mealPlan,
            nutritionSummary: nutritionSummary,
            userData: userData
        });

        await user.save();

        res.json({ message: 'Meal plan saved successfully' });
    } catch (err) {
        res.status(500).json({ message: 'Error saving meal plan', error: err.message });
    }
});

// Get user's meal plans
app.get('/meal-plans/:email', async (req, res) => {
    const { email } = req.params;

    try {
        const user = await UserModel.findOne({ email });
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        res.json(user.mealPlans);
    } catch (err) {
        res.status(500).json({ message: 'Error fetching meal plans', error: err.message });
    }
});

app.listen(3001, () => {
    console.log('Server is running on port 3001');
});

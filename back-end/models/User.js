


const mongoose = require('mongoose');

// const UserSchema = new mongoose.Schema({
//     firstName: { type: String, required: true },
//     lastName: { type: String, required: true },
//     email: { type: String, required: true },
//     password: { type: String, required: true },
//
//
// });




const userSchema = new mongoose.Schema({
    firstName: String,
    lastName: String,
    email: { type: String, unique: true },
    password: String,
    mealPlans: [{
        createdAt: { type: Date, default: Date.now },
        planData: Object,
        nutritionSummary: Object,
        userData: Object
    }]
});

module.exports = mongoose.model('User', userSchema);

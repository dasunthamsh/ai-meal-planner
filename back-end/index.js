

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








// sign up user (add user)

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










app.listen(3001, () => {
    console.log('Server is running on port 3001');
});

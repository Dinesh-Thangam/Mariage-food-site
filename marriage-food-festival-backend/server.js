const express = require('express');
const cors = require('cors');
require('dotenv').config();
const mongoose = require('mongoose');

console.log('MONGO_URI:', process.env.MONGO_URI ? 'Exists' : 'Missing');
console.log('JWT_SECRET:', process.env.JWT_SECRET ? 'Exists' : 'Missing');

const app = express();

// Middleware to allow cross-origin requests and parse JSON bodies
app.use(cors());
app.use(express.json());
const authRoutes = require('./routes/auth');
app.use('/api/auth', authRoutes);

// Define a simple route to test the server
app.get('/', (req, res) => {
  res.send('Marriage Food Festival Backend Running');
});

// Connect to MongoDB and start server only after successful connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  console.log('MongoDB connected');

  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
})
.catch(err => {
  console.error('MongoDB connection error:', err);
});

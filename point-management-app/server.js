const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// In-memory database
const users = {};

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Point Management API',
    status: 'active',
    version: '1.0.0'
  });
});

// Health check endpoint for container health checks
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP' });
});

// Get all users with their points
app.get('/api/users', (req, res) => {
  res.json(Object.values(users));
});

// Get a specific user
app.get('/api/users/:id', (req, res) => {
  const user = users[req.params.id];
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

// Create a new user
app.post('/api/users', (req, res) => {
  const { name } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'Name is required' });
  }

  const id = uuidv4();
  const newUser = {
    id,
    name,
    points: 0,
    createdAt: new Date().toISOString()
  };

  users[id] = newUser;
  res.status(201).json(newUser);
});

// Update user points
app.patch('/api/users/:id/points', (req, res) => {
  const { points } = req.body;
  const user = users[req.params.id];

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  if (points === undefined || isNaN(points)) {
    return res.status(400).json({ error: 'Valid points value is required' });
  }

  user.points = parseInt(points);
  user.updatedAt = new Date().toISOString();

  res.json(user);
});

// Add points to a user
app.post('/api/users/:id/points', (req, res) => {
  const { points } = req.body;
  const user = users[req.params.id];

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  if (points === undefined || isNaN(points)) {
    return res.status(400).json({ error: 'Valid points value is required' });
  }

  user.points += parseInt(points);
  user.updatedAt = new Date().toISOString();

  res.json(user);
});

// Delete a user
app.delete('/api/users/:id', (req, res) => {
  const user = users[req.params.id];
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  delete users[req.params.id];
  res.status(204).end();
});

// Only start the server if this file is run directly
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Point Management API running on port ${PORT}`);
  });
}

// Export for testing
module.exports = app;
const request = require('supertest');
const app = require('../server');

describe('Point Management API', () => {
  let userId;

  // Test the root endpoint
  describe('GET /', () => {
    it('should return API information', async () => {
      const res = await request(app).get('/');
      expect(res.statusCode).toEqual(200);
      expect(res.body).toHaveProperty('message');
      expect(res.body).toHaveProperty('status');
      expect(res.body.status).toEqual('active');
    });
  });

  // Test health check endpoint
  describe('GET /health', () => {
    it('should return UP status', async () => {
      const res = await request(app).get('/health');
      expect(res.statusCode).toEqual(200);
      expect(res.body).toHaveProperty('status');
      expect(res.body.status).toEqual('UP');
    });
  });

  // Test user creation
  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const res = await request(app)
        .post('/api/users')
        .send({ name: 'Test User' });
      
      expect(res.statusCode).toEqual(201);
      expect(res.body).toHaveProperty('id');
      expect(res.body).toHaveProperty('name');
      expect(res.body).toHaveProperty('points');
      expect(res.body.name).toEqual('Test User');
      expect(res.body.points).toEqual(0);
      
      // Save the user ID for later tests
      userId = res.body.id;
    });

    it('should return 400 if name is missing', async () => {
      const res = await request(app)
        .post('/api/users')
        .send({});
      
      expect(res.statusCode).toEqual(400);
      expect(res.body).toHaveProperty('error');
    });
  });

  // Test get all users
  describe('GET /api/users', () => {
    it('should return all users', async () => {
      const res = await request(app).get('/api/users');
      
      expect(res.statusCode).toEqual(200);
      expect(Array.isArray(res.body)).toBeTruthy();
      expect(res.body.length).toBeGreaterThan(0);
    });
  });

  // Test get specific user
  describe('GET /api/users/:id', () => {
    it('should get a user by ID', async () => {
      const res = await request(app).get(`/api/users/${userId}`);
      
      expect(res.statusCode).toEqual(200);
      expect(res.body).toHaveProperty('id');
      expect(res.body.id).toEqual(userId);
    });

    it('should return 404 for non-existent user', async () => {
      const res = await request(app).get('/api/users/nonexistent-id');
      
      expect(res.statusCode).toEqual(404);
    });
  });

  // Test updating user points
  describe('PATCH /api/users/:id/points', () => {
    it('should update a user\'s points', async () => {
      const res = await request(app)
        .patch(`/api/users/${userId}/points`)
        .send({ points: 100 });
      
      expect(res.statusCode).toEqual(200);
      expect(res.body).toHaveProperty('points');
      expect(res.body.points).toEqual(100);
    });

    it('should return 400 for invalid points', async () => {
      const res = await request(app)
        .patch(`/api/users/${userId}/points`)
        .send({ points: 'invalid' });
      
      expect(res.statusCode).toEqual(400);
    });
  });

  // Test adding points to a user
  describe('POST /api/users/:id/points', () => {
    it('should add points to a user', async () => {
      const res = await request(app)
        .post(`/api/users/${userId}/points`)
        .send({ points: 50 });
      
      expect(res.statusCode).toEqual(200);
      expect(res.body).toHaveProperty('points');
      expect(res.body.points).toEqual(150); // 100 from previous test + 50
    });
  });

  // Test user deletion
  describe('DELETE /api/users/:id', () => {
    it('should delete a user', async () => {
      const res = await request(app).delete(`/api/users/${userId}`);
      
      expect(res.statusCode).toEqual(204);
    });

    it('should return 404 after deletion', async () => {
      const res = await request(app).get(`/api/users/${userId}`);
      
      expect(res.statusCode).toEqual(404);
    });
  });
});
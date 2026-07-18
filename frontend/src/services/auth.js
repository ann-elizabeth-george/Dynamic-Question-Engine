import api from './api';

export const registerUser = (data) => api.post('/auth/register', data);

export const loginUser = (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  return api.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
};

export const getMe = () => api.get('/auth/me');

export const createProfile = (data) => api.post('/auth/profile', data);

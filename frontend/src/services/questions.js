import api from './api';

export const createQuestion = (data) => api.post('/questions', data);
export const getQuestionsByCategory = (categoryId) => api.get(`/questions/category/${categoryId}`);

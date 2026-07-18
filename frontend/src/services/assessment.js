import api from './api';

export const startAssessment = (categoryId) => api.post('/assessment/start', { category_id: categoryId });
export const getCurrentQuestion = (sessionId) => api.get(`/assessment/question?session_id=${sessionId}`);
export const submitAnswer = (data) => api.post('/assessment/answer', data);
export const getAssessmentHistory = () => api.get('/assessment/history');

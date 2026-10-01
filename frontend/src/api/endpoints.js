import api from './client';

export const authLogin = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const authRegister = async (email, password, full_name) => {
  const response = await api.post('/auth/register', { email, password, full_name });
  return response.data;
};

export const getMe = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const getDestinations = async (params = {}) => {
  const response = await api.get('/destinations', { params });
  return response.data;
};

export const getDestinationById = async (id) => {
  const response = await api.get(`/destinations/${id}`);
  return response.data;
};

export const sendChatMessage = async (message, conversation_id = null) => {
  const response = await api.post('/chat', { message, conversation_id });
  return response.data;
};

export const getUserTrips = async () => {
  const response = await api.get('/trips');
  return response.data;
};

export const saveUserTrip = async (tripData) => {
  const response = await api.post('/trips', tripData);
  return response.data;
};

export const getUserPreferences = async () => {
  const response = await api.get('/users/preferences');
  return response.data;
};

export const updateUserPreferences = async (preferences) => {
  const response = await api.put('/users/preferences', preferences);
  return response.data;
};

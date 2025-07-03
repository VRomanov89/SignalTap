import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

export const scanTags = async (ip, slot = 0) => {
  try {
    const response = await api.get(`/scan-simple?ip=${ip}&slot=${slot}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to scan PLC tags');
  }
};

export const readTags = async (ip, tags) => {
  try {
    const response = await api.post('/read-tags', { ip, tags });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to read PLC tags');
  }
};

export default api; 
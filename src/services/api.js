import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
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
  // Placeholder: implement API call to /read-tags
  // return await api.post('/read-tags', { ip, tags });
  return [];
};

export default api; 
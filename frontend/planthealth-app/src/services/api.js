import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const predictImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append('imagen', file);

    const response = await api.post('/api/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      throw new Error(error.response.data?.detail || 'Error from server');
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error('No response from server. Check if backend is running.');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new Error('Error preparing the request: ' + error.message);
    }
  }
};

import { useState } from 'react';
import { predictImage } from '../services/api';

export const usePredict = () => {
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const analyzeImage = async (file) => {
    setStatus('loading');
    setError(null);
    try {
      const data = await predictImage(file);
      setResult(data);
      setStatus('success');
    } catch (err) {
      setError(err.message);
      setStatus('error');
    }
  };

  const reset = () => {
    setStatus('idle');
    setResult(null);
    setError(null);
  };

  return { analyzeImage, status, result, error, reset };
};

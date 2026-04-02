export const API_BASE_URL = 'http://localhost:8000/api';

// Helper function for API calls
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage = errorData.detail || errorData.error || JSON.stringify(errorData) || `API Error: ${response.statusText}`;
    console.error('API Error:', errorMessage, errorData);
    throw new Error(errorMessage);
  }
  
  return response.json();
};


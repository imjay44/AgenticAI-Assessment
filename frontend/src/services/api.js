import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://banking-intelligence-backend.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auto-inject JWT token from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Don't auto-redirect if trying to login
      if (!error.config.url.includes('/auth/login')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const res = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },
  register: async (userData) => {
    const res = await api.post('/auth/register', userData);
    return res.data;
  },
  getMe: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  }
};

export const businessAPI = {
  getProfile: async () => {
    const res = await api.get('/business-profile');
    return res.data;
  },
  updateProfile: async (data) => {
    const res = await api.put('/business-profile', data);
    return res.data;
  }
};

export const analyticsAPI = {
  getOverview: async () => {
    const res = await api.get('/analytics/overview');
    return res.data;
  },
  getMonthlyTrends: async () => {
    const res = await api.get('/analytics/monthly-trends');
    return res.data;
  }
};

export const datasetAPI = {
  getStats: async () => {
    const res = await api.get('/dataset/stats');
    return res.data;
  },
  getPreview: async (tableName, limit = 25) => {
    const res = await api.get(`/dataset/preview/${tableName}?limit=${limit}`);
    return res.data;
  },
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post('/dataset/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  }
};

export const agentsAPI = {
  getSpecs: async () => {
    const res = await api.get('/agents/specs');
    return res.data;
  },
  runWorkflow: async (options = {}) => {
    const res = await api.post('/agents/run', options);
    return res.data;
  },
  getStatus: async (sessionId) => {
    const res = await api.get(`/agents/status/${sessionId}`);
    return res.data;
  },
  getLogs: async (sessionId = null) => {
    const url = sessionId ? `/agents/logs?session_id=${sessionId}` : '/agents/logs';
    const res = await api.get(url);
    return res.data;
  }
};

export const chatAPI = {
  ask: async (message, sessionId = null, targetAgent = 'Strategy Agent') => {
    const res = await api.post('/chat', {
      message,
      session_id: sessionId,
      target_agent: targetAgent
    });
    return res.data;
  }
};

export const reportsAPI = {
  list: async () => {
    const res = await api.get('/reports');
    return res.data;
  },
  getDetails: async (reportId) => {
    const res = await api.get(`/reports/${reportId}`);
    return res.data;
  },
  getDownloadUrl: (reportId) => {
    const token = localStorage.getItem('token');
    return `${API_BASE_URL}/reports/${reportId}/download?token=${token || ''}`;
  }
};

export const approvalsAPI = {
  list: async (statusFilter = null) => {
    const url = statusFilter ? `/approvals?status_filter=${statusFilter}` : '/approvals';
    const res = await api.get(url);
    return res.data;
  },
  takeAction: async (approvalId, decision, reviewNotes = '') => {
    const res = await api.post(`/approvals/${approvalId}/action`, {
      decision,
      review_notes: reviewNotes
    });
    return res.data;
  }
};

export const adminAPI = {
  getUsers: async () => {
    const res = await api.get('/admin/users');
    return res.data;
  },
  createUser: async (userData) => {
    const res = await api.post('/admin/users', userData);
    return res.data;
  },
  deleteUser: async (userId) => {
    const res = await api.delete(`/admin/users/${userId}`);
    return res.data;
  },
  getSystemHealth: async () => {
    const res = await api.get('/admin/system-health');
    return res.data;
  }
};

export default api;

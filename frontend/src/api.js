import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/',
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    if (
      error.response?.status === 401 &&
      window.location.pathname !== '/login' &&
      window.location.pathname !== '/register'
    ) {
      localStorage.clear();
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export const login = (email, password) =>
  api.post('/auth/login', { email, password });

export const register = data =>
  api.post('/auth/register', data);

export const getMe = () =>
  api.get('/auth/me');

export const sendMessage = (
  message,
  enquiryId,
  buyerName,
  buyerPhone,
  buyerEmail
) =>
  api.post('/chat/message', {
    message,
    enquiry_id: enquiryId,
    buyer_name: buyerName,
    buyer_phone: buyerPhone,
    buyer_email: buyerEmail
  });

export const getChatHistory = id =>
  api.get(`/chat/history/${id}`);

export const bookVisit = data =>
  api.post('/visits/book', data);

export const listVisits = status =>
  api.get('/visits/list', {
    params: status ? { status } : {}
  });

export const myVisits = () =>
  api.get('/visits/my-visits');

export const updateVisitStatus = (id, status) =>
  api.patch(`/visits/${id}/status`, null, {
    params: { new_status: status }
  });

export const postponeVisit = (id, data) =>
  api.post(`/visits/${id}/postpone`, data);

export const submitVisitFeedback = (id, feedback, rating) =>
  api.post(`/visits/${id}/feedback`, {
    feedback,
    rating
  });

export const listEnquiries = status =>
  api.get('/enquiries/list', {
    params: status ? { status } : {}
  });

export const updateEnquiry = (id, data) =>
  api.patch(`/enquiries/${id}`, data);

export const createEnquiry = data =>
  api.post('/enquiries/create', data);

export const getEnquiryStats = () =>
  api.get('/enquiries/stats/summary');

export const listProperties = () =>
  api.get('/properties/list');

export const createProperty = data =>
  api.post('/properties/create', data);

export const deleteProperty = id =>
  api.delete(`/properties/${id}`);

export const listNotifications = () =>
  api.get('/notifications/list');

export const markAllRead = () =>
  api.post('/notifications/read-all');

export const getUnreadCount = () =>
  api.get('/notifications/unread-count');

export const getActivityFeed = () =>
  api.get('/activity/feed');

export default api;

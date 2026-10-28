import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

function getAuthToken(): string | undefined {
  if (typeof document === 'undefined') return undefined;
  return document.cookie
    .split('; ')
    .find((row) => row.startsWith('auth-token='))
    ?.split('=')[1];
}

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function login(credentials: any) {
  const response = await api.post('/users/login', credentials);
  return response.data;
}

export async function getUsers() {
  const response = await api.get('/users/');
  return response.data;
}

export async function createUser(user: any) {
  const response = await api.post('/users/', user);
  return response.data;
}

export async function updateUser(userId: string, data: any) {
  const response = await api.put(`/users/${userId}`, data);
  return response.data;
}

export async function toggleUserStatus(userId: string) {
  const response = await api.patch(`/users/${userId}/toggle-status`);
  return response.data;
}

export async function getRoles() {
  const response = await api.get('/roles/');
  return response.data;
}
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
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
import { api } from './base';

/**
 * Authenticates the user and returns the login response containing the token.
 */
export async function login(credentials: any) {
  const response = await api.post('/users/login', credentials);
  return response.data;
}

/**
 * Retrieves a list of all users from the database.
 */
export async function getUsers() {
  const response = await api.get('/users/');
  return response.data;
}

/**
 * Creates a new user in the system.
 */
export async function createUser(user: any) {
  const response = await api.post('/users/', user);
  return response.data;
}

/**
 * Updates an existing user's data.
 */
export async function updateUser(userId: string, data: any) {
  const response = await api.put(`/users/${userId}`, data);
  return response.data;
}

/**
 * Toggles the active/inactive status of a specific user.
 */
export async function toggleUserStatus(userId: string) {
  const response = await api.patch(`/users/${userId}/toggle-status`);
  return response.data;
}

/**
 * Retrieves all available roles from the system.
 */
export async function getRoles() {
  const response = await api.get('/roles/');
  return response.data;
}
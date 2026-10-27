import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

/**
 * Intercepts Axios requests to automatically attach the JWT Bearer token.
 * It reads the 'auth-token' from browser cookies and appends it to the Authorization header.
 * 
 * @param config - The Axios request configuration object.
 * @returns The modified Axios request configuration.
 */
api.interceptors.request.use(
  (config) => {
    if (typeof document !== 'undefined') {
      const match = document.cookie.match(new RegExp('(^| )auth-token=([^;]+)'));
      if (match && match[2]) {
        config.headers.Authorization = `Bearer ${match[2]}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

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
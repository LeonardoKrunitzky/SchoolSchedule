import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use(
  async (config) => {
    let token;

    if (typeof window !== 'undefined') {
      const match = document.cookie.match(new RegExp('(^| )auth-token=([^;]+)'));
      if (match && match[2]) {
        token = match[2];
      }
    } else {
      const { cookies } = await import('next/headers');
      const cookieStore = await cookies();
      token = cookieStore.get('auth-token')?.value;
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);
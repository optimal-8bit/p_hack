import { apiClient } from '../lib/apiClient'

export const authService = {
  register: (payload) => apiClient.post('/auth/register', payload),
  login: (payload) => apiClient.post('/auth/login', payload),
  loginWithGoogle: (idToken) => apiClient.post('/auth/google', { id_token: idToken }),
  me: () => apiClient.get('/auth/me'),
}

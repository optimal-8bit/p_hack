import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: {
    name: 'Dr. John Smith',
    email: 'doctor@example.com',
    phone: '+1234567890',
    role: 'doctor'
  },
  updateUser: (userData) => set({ user: userData }),
}));

// Mock auth service
export const authService = {
  updateProfile: async (data) => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return { ...data, email: 'doctor@example.com' };
  },
};

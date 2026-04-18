import apiClient from './api.service';

export const doctorService = {
  getDashboard: async (doctorId = 'doc-001') => {
    try {
      const response = await apiClient.get(`/api/doctor/dashboard?doctor_id=${doctorId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching doctor dashboard:', error);
      throw error;
    }
  },

  getAppointments: async (doctorId = 'doc-001') => {
    try {
      const response = await apiClient.get(`/api/doctor/appointments?doctor_id=${doctorId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching appointments:', error);
      throw error;
    }
  },

  updateAppointment: async (appointmentId, data) => {
    try {
      const response = await apiClient.patch(`/api/doctor/appointments/${appointmentId}`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating appointment:', error);
      throw error;
    }
  },

  getPatients: async (doctorId = 'doc-001') => {
    try {
      const response = await apiClient.get(`/api/doctor/patients?doctor_id=${doctorId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching patients:', error);
      throw error;
    }
  },

  getPrescriptions: async (doctorId = 'doc-001') => {
    try {
      const response = await apiClient.get(`/api/doctor/prescriptions?doctor_id=${doctorId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching prescriptions:', error);
      throw error;
    }
  },

  getRecommendations: async (sessionId) => {
    try {
      const response = await apiClient.get(`/api/doctor/recommendations/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      throw error;
    }
  },

  searchDoctors: async (params = {}) => {
    try {
      const queryParams = new URLSearchParams(params).toString();
      const response = await apiClient.get(`/api/doctor/search?${queryParams}`);
      return response.data;
    } catch (error) {
      console.error('Error searching doctors:', error);
      throw error;
    }
  },
};

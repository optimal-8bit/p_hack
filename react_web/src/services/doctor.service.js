// Mock doctor service with sample data
const mockData = {
  dashboard: {
    metrics: {
      total_appointments: 156,
      todays_appointments: 8,
      pending_appointments: 12,
      total_prescriptions: 89,
    },
    ai_workload_summary: "Your workload is moderate this week with 8 appointments today. Peak hours are between 2-4 PM.",
    ai_recommendations: [
      "Consider scheduling buffer time between appointments",
      "Review pending lab results for 3 patients",
      "Follow up with patients from last week"
    ],
    todays_appointments: [
      { id: 1, scheduled_at: new Date().toISOString(), reason: "Regular Checkup", status: "confirmed" },
      { id: 2, scheduled_at: new Date(Date.now() + 3600000).toISOString(), reason: "Follow-up", status: "confirmed" },
      { id: 3, scheduled_at: new Date(Date.now() + 7200000).toISOString(), reason: "Consultation", status: "pending" },
    ],
    pending_appointments: [
      { id: 4, scheduled_at: new Date(Date.now() + 86400000).toISOString(), reason: "Initial Consultation", status: "pending" },
      { id: 5, scheduled_at: new Date(Date.now() + 172800000).toISOString(), reason: "Lab Results Review", status: "pending" },
    ]
  },
  appointments: [
    { id: 1, scheduled_at: new Date().toISOString(), reason: "Regular Checkup", status: "confirmed", notes: "Patient reports feeling better" },
    { id: 2, scheduled_at: new Date(Date.now() + 3600000).toISOString(), reason: "Follow-up", status: "confirmed" },
    { id: 3, scheduled_at: new Date(Date.now() + 7200000).toISOString(), reason: "Consultation", status: "pending" },
    { id: 4, scheduled_at: new Date(Date.now() + 86400000).toISOString(), reason: "Initial Consultation", status: "pending" },
  ],
  patients: [
    { id: 1, name: "John Doe", email: "john@example.com", phone: "+1234567890" },
    { id: 2, name: "Jane Smith", email: "jane@example.com", phone: "+1234567891" },
    { id: 3, name: "Mike Johnson", email: "mike@example.com", phone: "+1234567892" },
  ],
  prescriptions: [
    { id: 1, patient_id: 1, issued_at: new Date(Date.now() - 86400000).toISOString(), medicines: ["Medicine A", "Medicine B"], status: "active", notes: "Take after meals" },
    { id: 2, patient_id: 2, issued_at: new Date(Date.now() - 172800000).toISOString(), medicines: ["Medicine C"], status: "completed" },
  ]
};

export const doctorService = {
  getDashboard: async () => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.dashboard;
  },

  getAppointments: async () => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.appointments;
  },

  updateAppointment: async (id, data) => {
    await new Promise(resolve => setTimeout(resolve, 300));
    const appointment = mockData.appointments.find(a => a.id === id);
    if (appointment) {
      Object.assign(appointment, data);
    }
    return appointment;
  },

  getPatients: async () => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.patients;
  },

  getPrescriptions: async () => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockData.prescriptions;
  },
};

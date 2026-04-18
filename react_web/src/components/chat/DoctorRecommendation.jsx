import { useState, useEffect } from 'react';
import { Stethoscope, AlertCircle, Calendar, X, Clock, User } from 'lucide-react';
import { doctorService } from '@/services/doctor.service';

export default function DoctorRecommendation({ recommendation, sessionId }) {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showDoctors, setShowDoctors] = useState(false);
  const [dismissed, setDismissed] = useState(false);
  const [bookingDoctor, setBookingDoctor] = useState(null);
  const [appointmentForm, setAppointmentForm] = useState({
    date: '',
    time: '',
    reason: '',
    notes: ''
  });
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingSuccess, setBookingSuccess] = useState(false);

  useEffect(() => {
    if (showDoctors && recommendation?.specialization) {
      loadDoctors();
    }
  }, [showDoctors, recommendation]);

  const loadDoctors = async () => {
    setLoading(true);
    try {
      const results = await doctorService.searchDoctors({
        specialization: recommendation.specialization
      });
      setDoctors(results);
    } catch (error) {
      console.error('Error loading doctors:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBookAppointment = (doctor) => {
    setBookingDoctor(doctor);
    // Set default date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    setAppointmentForm({
      ...appointmentForm,
      date: tomorrow.toISOString().split('T')[0],
      reason: recommendation.reason || ''
    });
  };

  const handleSubmitAppointment = async (e) => {
    e.preventDefault();
    setBookingLoading(true);
    
    try {
      // Get current user from localStorage
      const authState = JSON.parse(localStorage.getItem('auth') || '{}');
      const currentUser = authState.user;
      
      // Prepare appointment data
      const appointmentData = {
        doctor_id: bookingDoctor.id,
        patient_id: currentUser?.id || null,
        session_id: sessionId,
        scheduled_date: appointmentForm.date,
        scheduled_time: appointmentForm.time,
        reason: appointmentForm.reason,
        notes: appointmentForm.notes || null,
      };
      
      console.log('📅 Booking appointment:', appointmentData);
      
      // Call backend API
      const result = await doctorService.bookAppointment(appointmentData);
      
      console.log('✅ Appointment booked successfully:', result);
      
      setBookingSuccess(true);
      setTimeout(() => {
        setBookingDoctor(null);
        setBookingSuccess(false);
        setAppointmentForm({ date: '', time: '', reason: '', notes: '' });
      }, 2000);
    } catch (error) {
      console.error('❌ Error booking appointment:', error);
      alert('Failed to book appointment. Please try again.');
    } finally {
      setBookingLoading(false);
    }
  };

  if (dismissed || !recommendation?.should_recommend) {
    return null;
  }

  const getUrgencyColor = (urgency) => {
    switch (urgency) {
      case 'urgent':
        return { bg: 'rgba(239, 68, 68, 0.1)', border: 'rgba(239, 68, 68, 0.3)', text: '#ef4444' };
      case 'high':
        return { bg: 'rgba(251, 191, 36, 0.1)', border: 'rgba(251, 191, 36, 0.3)', text: '#fbbf24' };
      default:
        return { bg: 'rgba(59, 130, 246, 0.1)', border: 'rgba(59, 130, 246, 0.3)', text: '#3b82f6' };
    }
  };

  const urgencyColors = getUrgencyColor(recommendation.urgency);

  return (
    <>
      <div style={{
        margin: '16px 0',
        padding: '20px',
        background: urgencyColors.bg,
        border: `1px solid ${urgencyColors.border}`,
        borderRadius: 12,
        position: 'relative',
      }}>
        <button
          onClick={() => setDismissed(true)}
          style={{
            position: 'absolute',
            top: 12,
            right: 12,
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            color: 'rgba(255,255,255,0.5)',
            padding: 4,
          }}
        >
          <X style={{ width: 18, height: 18 }} />
        </button>

        <div style={{ display: 'flex', alignItems: 'start', gap: 16 }}>
          <div style={{
            width: 48,
            height: 48,
            borderRadius: 12,
            background: urgencyColors.bg,
            border: `2px solid ${urgencyColors.border}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}>
            <Stethoscope style={{ width: 24, height: 24, color: urgencyColors.text }} />
          </div>

          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              <h4 style={{ fontSize: 16, fontWeight: 700, color: '#ffffff', margin: 0 }}>
                Professional Support Recommended
              </h4>
              {recommendation.urgency === 'urgent' && (
                <span style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 4,
                  padding: '4px 8px',
                  background: 'rgba(239, 68, 68, 0.2)',
                  borderRadius: 6,
                  fontSize: 11,
                  fontWeight: 600,
                  color: '#ef4444',
                }}>
                  <AlertCircle style={{ width: 12, height: 12 }} />
                  Urgent
                </span>
              )}
            </div>

            <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: 14, lineHeight: 1.6, marginBottom: 16 }}>
              {recommendation.reason}
            </p>

            {recommendation.specialization && (
              <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 13, marginBottom: 16 }}>
                Recommended specialist: <span style={{ color: urgencyColors.text, fontWeight: 600 }}>
                  {recommendation.specialization.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
              </p>
            )}

            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
              <button
                onClick={() => setShowDoctors(!showDoctors)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '10px 20px',
                  background: urgencyColors.text,
                  color: 'white',
                  border: 'none',
                  borderRadius: 8,
                  fontSize: 14,
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
              >
                <Calendar style={{ width: 16, height: 16 }} />
                {showDoctors ? 'Hide Doctors' : 'Find a Doctor'}
              </button>

              {recommendation.urgency === 'urgent' && (
                <a
                  href="tel:988"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8,
                    padding: '10px 20px',
                    background: 'rgba(239, 68, 68, 0.2)',
                    color: '#ef4444',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    borderRadius: 8,
                    fontSize: 14,
                    fontWeight: 600,
                    textDecoration: 'none',
                    transition: 'all 0.2s',
                  }}
                >
                  <AlertCircle style={{ width: 16, height: 16 }} />
                  Call Crisis Line (988)
                </a>
              )}
            </div>

            {showDoctors && (
              <div style={{ marginTop: 20, paddingTop: 20, borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                {loading ? (
                  <div style={{ textAlign: 'center', padding: '20px 0' }}>
                    <div style={{
                      width: 32,
                      height: 32,
                      border: '3px solid rgba(255,255,255,0.2)',
                      borderTop: '3px solid #ffffff',
                      borderRadius: '50%',
                      animation: 'spin 1s linear infinite',
                      margin: '0 auto',
                    }}></div>
                  </div>
                ) : doctors.length > 0 ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    <h5 style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.8)', marginBottom: 8 }}>
                      Available Specialists:
                    </h5>
                    {doctors.map((doctor) => (
                      <div key={doctor.id} style={{
                        padding: '16px',
                        background: 'rgba(255,255,255,0.05)',
                        borderRadius: 10,
                        border: '1px solid rgba(255,255,255,0.1)',
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 8 }}>
                          <div>
                            <h6 style={{ fontSize: 15, fontWeight: 600, color: '#ffffff', marginBottom: 4 }}>
                              {doctor.name}
                            </h6>
                            <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.6)' }}>
                              {doctor.specialization?.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </p>
                          </div>
                          {doctor.rating > 0 && (
                            <div style={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: 4,
                              padding: '4px 8px',
                              background: 'rgba(251, 191, 36, 0.1)',
                              borderRadius: 6,
                            }}>
                              <span style={{ color: '#fbbf24', fontSize: 14 }}>⭐</span>
                              <span style={{ color: '#fbbf24', fontSize: 13, fontWeight: 600 }}>
                                {doctor.rating.toFixed(1)}
                              </span>
                            </div>
                          )}
                        </div>
                        {doctor.bio && (
                          <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.7)', lineHeight: 1.5, marginBottom: 12 }}>
                            {doctor.bio}
                          </p>
                        )}
                        <div style={{ display: 'flex', gap: 8, fontSize: 12, color: 'rgba(255,255,255,0.6)', marginBottom: 12 }}>
                          {doctor.experience_years > 0 && (
                            <span>{doctor.experience_years} years experience</span>
                          )}
                          {doctor.total_reviews > 0 && (
                            <span>• {doctor.total_reviews} reviews</span>
                          )}
                        </div>
                        <button
                          onClick={() => handleBookAppointment(doctor)}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 8,
                            padding: '8px 16px',
                            background: urgencyColors.text,
                            color: 'white',
                            border: 'none',
                            borderRadius: 6,
                            fontSize: 13,
                            fontWeight: 600,
                            cursor: 'pointer',
                            transition: 'all 0.2s',
                          }}
                        >
                          <Calendar style={{ width: 14, height: 14 }} />
                          Book Appointment
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ color: 'rgba(255,255,255,0.6)', textAlign: 'center', padding: '20px 0' }}>
                    No doctors found. Please contact your healthcare provider.
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Appointment Booking Modal */}
      {bookingDoctor && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '20px',
        }}>
          <div style={{
            background: '#1a1a1a',
            borderRadius: 16,
            padding: '24px',
            maxWidth: 500,
            width: '100%',
            border: '1px solid rgba(255,255,255,0.1)',
          }}>
            {bookingSuccess ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <div style={{ fontSize: 48, marginBottom: 16 }}>✅</div>
                <h3 style={{ color: '#ffffff', marginBottom: 8 }}>Appointment Booked!</h3>
                <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 14 }}>
                  You'll receive a confirmation email shortly.
                </p>
              </div>
            ) : (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 20 }}>
                  <div>
                    <h3 style={{ color: '#ffffff', marginBottom: 4 }}>Book Appointment</h3>
                    <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 14 }}>
                      with {bookingDoctor.name}
                    </p>
                  </div>
                  <button
                    onClick={() => setBookingDoctor(null)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: 'rgba(255,255,255,0.5)',
                      cursor: 'pointer',
                      padding: 4,
                    }}
                  >
                    <X style={{ width: 20, height: 20 }} />
                  </button>
                </div>

                <form onSubmit={handleSubmitAppointment} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                  <div>
                    <label style={{ display: 'block', color: 'rgba(255,255,255,0.8)', fontSize: 13, marginBottom: 8 }}>
                      Preferred Date*
                    </label>
                    <input
                      type="date"
                      required
                      value={appointmentForm.date}
                      onChange={(e) => setAppointmentForm({ ...appointmentForm, date: e.target.value })}
                      min={new Date().toISOString().split('T')[0]}
                      style={{
                        width: '100%',
                        padding: '10px 12px',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        color: '#ffffff',
                        fontSize: 14,
                      }}
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', color: 'rgba(255,255,255,0.8)', fontSize: 13, marginBottom: 8 }}>
                      Preferred Time*
                    </label>
                    <input
                      type="time"
                      required
                      value={appointmentForm.time}
                      onChange={(e) => setAppointmentForm({ ...appointmentForm, time: e.target.value })}
                      style={{
                        width: '100%',
                        padding: '10px 12px',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        color: '#ffffff',
                        fontSize: 14,
                      }}
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', color: 'rgba(255,255,255,0.8)', fontSize: 13, marginBottom: 8 }}>
                      Reason for Visit*
                    </label>
                    <textarea
                      required
                      value={appointmentForm.reason}
                      onChange={(e) => setAppointmentForm({ ...appointmentForm, reason: e.target.value })}
                      rows={3}
                      style={{
                        width: '100%',
                        padding: '10px 12px',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        color: '#ffffff',
                        fontSize: 14,
                        fontFamily: 'inherit',
                        resize: 'vertical',
                      }}
                    />
                  </div>

                  <div>
                    <label style={{ display: 'block', color: 'rgba(255,255,255,0.8)', fontSize: 13, marginBottom: 8 }}>
                      Additional Notes (Optional)
                    </label>
                    <textarea
                      value={appointmentForm.notes}
                      onChange={(e) => setAppointmentForm({ ...appointmentForm, notes: e.target.value })}
                      rows={2}
                      placeholder="Any specific concerns or questions..."
                      style={{
                        width: '100%',
                        padding: '10px 12px',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        color: '#ffffff',
                        fontSize: 14,
                        fontFamily: 'inherit',
                        resize: 'vertical',
                      }}
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={bookingLoading}
                    style={{
                      padding: '12px 20px',
                      background: bookingLoading ? 'rgba(59, 130, 246, 0.5)' : urgencyColors.text,
                      color: 'white',
                      border: 'none',
                      borderRadius: 8,
                      fontSize: 14,
                      fontWeight: 600,
                      cursor: bookingLoading ? 'not-allowed' : 'pointer',
                      marginTop: 8,
                    }}
                  >
                    {bookingLoading ? 'Booking...' : 'Confirm Appointment'}
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}

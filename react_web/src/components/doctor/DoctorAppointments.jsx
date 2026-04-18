import { useState, useEffect } from 'react';
import { doctorService } from '@/services/doctor.service';
import { formatDateTime, getStatusColor, handleApiError } from '@/lib/utils';
import { Calendar, Check, X } from 'lucide-react';
import DoctorLayout from './DoctorLayout';
import BorderGlow from '../ui/BorderGlow';
import MorphingLoader from '../MorphingLoader';

export default function DoctorAppointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments = async () => {
    try {
      const data = await doctorService.getAppointments();
      setAppointments(data);
    } catch (err) {
      console.error(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (id, status) => {
    try {
      await doctorService.updateAppointment(id, { status });
      loadAppointments();
    } catch (err) {
      alert(handleApiError(err));
    }
  };

  return (
    <DoctorLayout title="Appointments" icon={Calendar}>
      {loading ? (
        <MorphingLoader 
          size="lg" 
          color="yellow" 
          message="Loading appointments..."
        />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {appointments.length > 0 ? (
            appointments.map((appt) => (
              <BorderGlow key={appt.id} glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
                <div style={{ padding: '1.5rem' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                      <Calendar style={{ width: 20, height: 20, color: '#3b82f6' }} />
                      <span style={{ fontSize: 16, fontWeight: 600, color: '#ffffff' }}>
                        {formatDateTime(appt.scheduled_at)}
                      </span>
                      <span style={{ padding: '4px 12px', borderRadius: 20, fontSize: 11, fontWeight: 600 }}
                        className={getStatusColor(appt.status)}>
                        {appt.status}
                      </span>
                    </div>
                    <div style={{
                      padding: '1rem', background: 'rgba(255,255,255,0.05)',
                      borderRadius: 12, border: '1px solid rgba(255,255,255,0.1)',
                    }}>
                      <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 13, marginBottom: 4 }}>
                        <span style={{ fontWeight: 600 }}>Reason:</span>
                      </p>
                      <p style={{ color: '#ffffff', fontSize: 14 }}>{appt.reason || 'General Consultation'}</p>
                    </div>
                    {appt.notes && (
                      <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 13, fontStyle: 'italic' }}>
                        <span style={{ fontWeight: 600 }}>Notes:</span> {appt.notes}
                      </p>
                    )}
                    {appt.status === 'pending' && (
                      <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
                        <button
                          onClick={() => handleUpdateStatus(appt.id, 'confirmed')}
                          style={{
                            display: 'flex', alignItems: 'center', gap: 8, padding: '10px 20px',
                            background: '#3b82f6', color: 'white', border: 'none', borderRadius: 8,
                            fontSize: 14, fontWeight: 600, cursor: 'pointer', transition: 'all 0.2s',
                          }}
                        >
                          <Check style={{ width: 16, height: 16 }} />
                          Confirm
                        </button>
                        <button
                          onClick={() => handleUpdateStatus(appt.id, 'cancelled')}
                          style={{
                            display: 'flex', alignItems: 'center', gap: 8, padding: '10px 20px',
                            background: 'rgba(255,255,255,0.1)', color: 'white',
                            border: '1px solid rgba(255,255,255,0.2)', borderRadius: 8,
                            fontSize: 14, fontWeight: 600, cursor: 'pointer', transition: 'all 0.2s',
                          }}
                        >
                          <X style={{ width: 16, height: 16 }} />
                          Cancel
                        </button>
                      </div>
                    )}
                    {appt.status === 'confirmed' && (
                      <button
                        onClick={() => handleUpdateStatus(appt.id, 'completed')}
                        style={{
                          padding: '10px 20px', background: '#3b82f6', color: 'white',
                          border: 'none', borderRadius: 8, fontSize: 14, fontWeight: 600,
                          cursor: 'pointer', transition: 'all 0.2s',
                        }}
                      >
                        Mark Complete
                      </button>
                    )}
                  </div>
                </div>
              </BorderGlow>
            ))
          ) : (
            <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
              <div style={{ padding: '4rem', textAlign: 'center' }}>
                <Calendar style={{ width: 64, height: 64, color: 'rgba(255,255,255,0.2)', margin: '0 auto 16px' }} />
                <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 16 }}>No appointments</p>
              </div>
            </BorderGlow>
          )}
        </div>
      )}
    </DoctorLayout>
  );
}

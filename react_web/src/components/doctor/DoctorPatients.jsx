import { useState, useEffect } from 'react';
import { doctorService } from '@/services/doctor.service';
import { handleApiError } from '@/lib/utils';
import { Users, Mail, Phone } from 'lucide-react';
import DoctorLayout from './DoctorLayout';
import BorderGlow from '../ui/BorderGlow';
import MorphingLoader from '../MorphingLoader';

export default function DoctorPatients() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    try {
      const data = await doctorService.getPatients();
      setPatients(data);
    } catch (err) {
      console.error(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <DoctorLayout title="My Patients" icon={Users}>
      {loading ? (
        <MorphingLoader 
          size="lg" 
          color="yellow" 
          message="Loading patients..."
        />
      ) : (
        <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
          <div style={{ padding: '2rem' }}>
            {patients.length > 0 ? (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
                {patients.map((patient) => (
                  <div key={patient.id} style={{
                    padding: '1.5rem',
                    background: 'rgba(255,255,255,0.05)',
                    borderRadius: 12,
                    border: '1px solid rgba(255,255,255,0.1)',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'start', gap: 16 }}>
                      <div style={{
                        width: 48, height: 48, borderRadius: 12,
                        background: 'rgba(59, 130, 246, 0.1)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                      }}>
                        <Users style={{ width: 24, height: 24, color: '#3b82f6' }} />
                      </div>
                      <div style={{ flex: 1 }}>
                        <h3 style={{ fontSize: 16, fontWeight: 600, color: '#ffffff', marginBottom: 12 }}>
                          {patient.name}
                        </h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                            <Mail style={{ width: 16, height: 16, color: 'rgba(255,255,255,0.6)' }} />
                            <span style={{ fontSize: 13, color: 'rgba(255,255,255,0.8)' }}>{patient.email}</span>
                          </div>
                          {patient.phone && (
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                              <Phone style={{ width: 16, height: 16, color: 'rgba(255,255,255,0.6)' }} />
                              <span style={{ fontSize: 13, color: 'rgba(255,255,255,0.8)' }}>{patient.phone}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ padding: '4rem', textAlign: 'center' }}>
                <Users style={{ width: 64, height: 64, color: 'rgba(255,255,255,0.2)', margin: '0 auto 16px' }} />
                <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 16 }}>No patients found</p>
              </div>
            )}
          </div>
        </BorderGlow>
      )}
    </DoctorLayout>
  );
}

import { useState, useEffect } from 'react';
import { doctorService } from '@/services/doctor.service';
import { formatDateTime, getStatusColor, handleApiError } from '@/lib/utils';
import { FileText, Pill } from 'lucide-react';
import DoctorLayout from './DoctorLayout';
import BorderGlow from '../ui/BorderGlow';

export default function DoctorPrescriptions() {
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPrescriptions();
  }, []);

  const loadPrescriptions = async () => {
    try {
      const data = await doctorService.getPrescriptions();
      setPrescriptions(data);
    } catch (err) {
      console.error(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <DoctorLayout title="Issued Prescriptions" icon={FileText}>
      {loading ? (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '400px' }}>
          <div style={{
            width: 48, height: 48, border: '4px solid rgba(124, 255, 103, 0.2)',
            borderTop: '4px solid #7cff67', borderRadius: '50%', animation: 'spin 1s linear infinite',
          }}></div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {prescriptions.length > 0 ? (
            prescriptions.map((rx) => (
              <BorderGlow key={rx.id} glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
                <div style={{ padding: '1.5rem' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                    <div style={{ display: 'flex', alignItems: 'start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
                      <div style={{ display: 'flex', alignItems: 'start', gap: 12 }}>
                        <div style={{
                          width: 48, height: 48, borderRadius: 12,
                          background: 'rgba(168, 85, 247, 0.1)',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                        }}>
                          <FileText style={{ width: 24, height: 24, color: '#a855f7' }} />
                        </div>
                        <div>
                          <p style={{ fontSize: 14, color: 'rgba(255,255,255,0.6)', marginBottom: 4 }}>
                            Issued: {formatDateTime(rx.issued_at)}
                          </p>
                          <p style={{ fontSize: 14, color: 'rgba(255,255,255,0.6)' }}>
                            Patient ID: {rx.patient_id}
                          </p>
                        </div>
                      </div>
                      <span style={{ padding: '4px 12px', borderRadius: 20, fontSize: 11, fontWeight: 600 }}
                        className={getStatusColor(rx.status)}>
                        {rx.status}
                      </span>
                    </div>

                    <div style={{
                      padding: '1rem', background: 'rgba(255,255,255,0.05)',
                      borderRadius: 12, border: '1px solid rgba(255,255,255,0.1)',
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                        <Pill style={{ width: 18, height: 18, color: '#a855f7' }} />
                        <p style={{ fontSize: 14, fontWeight: 600, color: '#ffffff', margin: 0 }}>
                          Medicines ({rx.medicines?.length || 0})
                        </p>
                      </div>
                      {rx.medicines && rx.medicines.length > 0 && (
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 6 }}>
                          {rx.medicines.map((med, idx) => (
                            <li key={idx} style={{ display: 'flex', gap: 8, color: 'rgba(255,255,255,0.8)', fontSize: 14 }}>
                              <span style={{ color: '#a855f7' }}>•</span>
                              <span>{med}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>

                    {rx.notes && (
                      <div style={{
                        padding: '1rem', background: 'rgba(255,255,255,0.05)',
                        borderRadius: 12, border: '1px solid rgba(255,255,255,0.1)',
                      }}>
                        <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.6)', marginBottom: 4, fontWeight: 600 }}>
                          Notes:
                        </p>
                        <p style={{ fontSize: 14, color: 'rgba(255,255,255,0.8)', margin: 0 }}>
                          {rx.notes}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </BorderGlow>
            ))
          ) : (
            <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
              <div style={{ padding: '4rem', textAlign: 'center' }}>
                <FileText style={{ width: 64, height: 64, color: 'rgba(255,255,255,0.2)', margin: '0 auto 16px' }} />
                <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 16 }}>No prescriptions issued yet</p>
              </div>
            </BorderGlow>
          )}
        </div>
      )}
    </DoctorLayout>
  );
}

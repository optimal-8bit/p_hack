import { useState, useEffect } from 'react';
import { doctorService } from '@/services/doctor.service';
import { formatDateTime, getStatusColor, handleApiError } from '@/lib/utils';
import { Calendar, FileText, Bell, Activity, Clock, LayoutDashboard } from 'lucide-react';
import { Link } from 'react-router-dom';
import DoctorLayout from './DoctorLayout';
import BorderGlow from '../ui/BorderGlow';
import MorphingLoader from '../MorphingLoader';

export default function DoctorDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await doctorService.getDashboard();
      setDashboard(data);
    } catch (err) {
      console.error(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const metrics = dashboard?.metrics || {};

  const StatCard = ({ icon: Icon, title, value, bgColor, iconColor }) => (
    <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
      <div style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <p style={{ fontSize: 14, color: 'rgba(255,255,255,0.6)', fontWeight: 500, marginBottom: 8 }}>{title}</p>
            <p style={{ fontSize: 32, fontWeight: 700, color: '#ffffff' }}>{value}</p>
          </div>
          <div style={{
            width: 56,
            height: 56,
            borderRadius: 12,
            background: bgColor,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Icon style={{ width: 28, height: 28, color: iconColor }} />
          </div>
        </div>
      </div>
    </BorderGlow>
  );

  return (
    <DoctorLayout title="Doctor Dashboard" icon={LayoutDashboard}>
      {loading ? (
        <MorphingLoader 
          size="lg" 
          color="yellow" 
          message="Loading dashboard data..."
        />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {/* Stats Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 20 }}>
            <StatCard
              icon={Calendar}
              title="Total Appointments"
              value={metrics.total_appointments || 0}
              bgColor="rgba(59, 130, 246, 0.1)"
              iconColor="#3b82f6"
            />
            <StatCard
              icon={Clock}
              title="Today's Appointments"
              value={metrics.todays_appointments || 0}
              bgColor="rgba(34, 197, 94, 0.1)"
              iconColor="#22c55e"
            />
            <StatCard
              icon={Bell}
              title="Pending Requests"
              value={metrics.pending_appointments || 0}
              bgColor="rgba(251, 191, 36, 0.1)"
              iconColor="#fbbf24"
            />
            <StatCard
              icon={FileText}
              title="Prescriptions Issued"
              value={metrics.total_prescriptions || 0}
              bgColor="rgba(168, 85, 247, 0.1)"
              iconColor="#a855f7"
            />
          </div>

          {/* AI Summary */}
          {dashboard?.ai_workload_summary && (
            <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
              <div style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                  <Activity style={{ width: 20, height: 20, color: '#3b82f6' }} />
                  <h3 style={{ fontSize: 18, fontWeight: 700, color: '#ffffff', margin: 0 }}>AI Workload Summary</h3>
                </div>
                <p style={{ color: 'rgba(255,255,255,0.8)', marginBottom: 16, lineHeight: 1.6 }}>{dashboard.ai_workload_summary}</p>
                {dashboard.ai_recommendations && dashboard.ai_recommendations.length > 0 && (
                  <div>
                    <p style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.6)', marginBottom: 8 }}>Recommendations:</p>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                      {dashboard.ai_recommendations.map((rec, idx) => (
                        <li key={idx} style={{ display: 'flex', gap: 8, marginBottom: 6, color: 'rgba(255,255,255,0.7)', fontSize: 14 }}>
                          <span style={{ color: '#3b82f6' }}>•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </BorderGlow>
          )}

          {/* Appointments Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 20 }}>
            {/* Today's Appointments */}
            <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
              <div style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
                  <h3 style={{ fontSize: 18, fontWeight: 700, color: '#ffffff', margin: 0 }}>Today's Appointments</h3>
                  <Link to="/doctor-appointments" style={{ fontSize: 14, color: '#7cff67', textDecoration: 'none' }}>View All →</Link>
                </div>
                <div>
                  {dashboard?.todays_appointments && dashboard.todays_appointments.length > 0 ? (
                    dashboard.todays_appointments.map(appt => (
                      <div key={appt.id} style={{
                        padding: '1rem',
                        background: 'rgba(255,255,255,0.05)',
                        borderRadius: 12,
                        marginBottom: 12,
                        border: '1px solid rgba(255,255,255,0.1)',
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                          <div>
                            <p style={{ fontSize: 14, fontWeight: 600, color: '#ffffff', marginBottom: 4 }}>
                              {formatDateTime(appt.scheduled_at)}
                            </p>
                            <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.6)' }}>{appt.reason || 'General Consultation'}</p>
                          </div>
                          <span style={{
                            padding: '4px 12px',
                            borderRadius: 20,
                            fontSize: 11,
                            fontWeight: 600,
                          }} className={getStatusColor(appt.status)}>
                            {appt.status}
                          </span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p style={{ color: 'rgba(255,255,255,0.5)', textAlign: 'center', padding: '2rem 0' }}>No appointments today</p>
                  )}
                </div>
              </div>
            </BorderGlow>

            {/* Pending Appointments */}
            <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
              <div style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
                  <h3 style={{ fontSize: 18, fontWeight: 700, color: '#ffffff', margin: 0 }}>Pending Appointments</h3>
                  <Link to="/doctor-appointments" style={{ fontSize: 14, color: '#7cff67', textDecoration: 'none' }}>View All →</Link>
                </div>
                <div>
                  {dashboard?.pending_appointments && dashboard.pending_appointments.length > 0 ? (
                    dashboard.pending_appointments.map(appt => (
                      <div key={appt.id} style={{
                        padding: '1rem',
                        background: 'rgba(255,255,255,0.05)',
                        borderRadius: 12,
                        marginBottom: 12,
                        border: '1px solid rgba(255,255,255,0.1)',
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                          <div>
                            <p style={{ fontSize: 14, fontWeight: 600, color: '#ffffff', marginBottom: 4 }}>
                              {formatDateTime(appt.scheduled_at)}
                            </p>
                            <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.6)' }}>{appt.reason || 'General Consultation'}</p>
                          </div>
                          <span style={{
                            padding: '4px 12px',
                            borderRadius: 20,
                            fontSize: 11,
                            fontWeight: 600,
                          }} className={getStatusColor(appt.status)}>
                            {appt.status}
                          </span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p style={{ color: 'rgba(255,255,255,0.5)', textAlign: 'center', padding: '2rem 0' }}>No pending appointments</p>
                  )}
                </div>
              </div>
            </BorderGlow>
          </div>
        </div>
      )}
    </DoctorLayout>
  );
}

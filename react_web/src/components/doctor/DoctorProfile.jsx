import { useState } from 'react';
import { authService } from '@/services/auth.service';
import { useAuthStore } from '@/store/useAuthStore';
import { handleApiError } from '@/lib/utils';
import { User, Mail, Phone, Save, UserCircle } from 'lucide-react';
import DoctorLayout from './DoctorLayout';
import BorderGlow from '../ui/BorderGlow';

export default function DoctorProfile() {
  const { user, updateUser } = useAuthStore();
  const [formData, setFormData] = useState({
    name: user?.name || 'Dr. John Smith',
    phone: user?.phone || '+1 (555) 123-4567',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const updated = await authService.updateProfile(formData);
      updateUser(updated);
      setMessage('Profile updated successfully');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage(handleApiError(err));
      setTimeout(() => setMessage(''), 3000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DoctorLayout title="My Profile" icon={UserCircle}>
      <div style={{ maxWidth: 600, margin: '0 auto' }}>
        <BorderGlow glowColor="210 60 40" backgroundColor="rgba(18, 15, 23, 0.85)">
          <div style={{ padding: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
              <div style={{
                width: 48, height: 48, borderRadius: 12,
                background: 'rgba(59, 130, 246, 0.1)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                <UserCircle style={{ width: 24, height: 24, color: '#3b82f6' }} />
              </div>
              <h3 style={{ fontSize: 20, fontWeight: 700, color: '#ffffff', margin: 0 }}>Personal Information</h3>
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              {message && (
                <div style={{
                  padding: '12px 16px',
                  borderRadius: 10,
                  fontSize: 14,
                  fontWeight: 500,
                  background: message.includes('success') ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                  color: message.includes('success') ? '#22c55e' : '#ef4444',
                  border: `1px solid ${message.includes('success') ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                }}>
                  {message}
                </div>
              )}

              <div>
                <label style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.8)', display: 'block', marginBottom: 8 }}>
                  Full Name
                </label>
                <div style={{ position: 'relative' }}>
                  <User style={{
                    position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                    width: 20, height: 20, color: 'rgba(255,255,255,0.4)',
                  }} />
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                    style={{
                      width: '100%', padding: '12px 12px 12px 44px', borderRadius: 10,
                      background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                      color: '#ffffff', fontSize: 14, outline: 'none', transition: 'all 0.2s',
                    }}
                    onFocus={(e) => e.target.style.borderColor = '#7cff67'}
                    onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.1)'}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.8)', display: 'block', marginBottom: 8 }}>
                  Email
                </label>
                <div style={{ position: 'relative' }}>
                  <Mail style={{
                    position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                    width: 20, height: 20, color: 'rgba(255,255,255,0.4)',
                  }} />
                  <input
                    type="email"
                    value={user?.email || 'doctor@mediscan.ai'}
                    disabled
                    style={{
                      width: '100%', padding: '12px 12px 12px 44px', borderRadius: 10,
                      background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)',
                      color: 'rgba(255,255,255,0.5)', fontSize: 14, cursor: 'not-allowed',
                    }}
                  />
                </div>
              </div>

              <div>
                <label style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.8)', display: 'block', marginBottom: 8 }}>
                  Phone
                </label>
                <div style={{ position: 'relative' }}>
                  <Phone style={{
                    position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                    width: 20, height: 20, color: 'rgba(255,255,255,0.4)',
                  }} />
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    style={{
                      width: '100%', padding: '12px 12px 12px 44px', borderRadius: 10,
                      background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                      color: '#ffffff', fontSize: 14, outline: 'none', transition: 'all 0.2s',
                    }}
                    onFocus={(e) => e.target.style.borderColor = '#7cff67'}
                    onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.1)'}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
                  padding: '14px 24px', borderRadius: 10, background: '#3b82f6',
                  color: 'white', fontSize: 15, fontWeight: 600, border: 'none',
                  cursor: loading ? 'not-allowed' : 'pointer', transition: 'all 0.2s',
                  opacity: loading ? 0.6 : 1, marginTop: 8,
                }}
                onMouseEnter={(e) => !loading && (e.currentTarget.style.background = '#2563eb')}
                onMouseLeave={(e) => !loading && (e.currentTarget.style.background = '#3b82f6')}
              >
                <Save style={{ width: 18, height: 18 }} />
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
            </form>
          </div>
        </BorderGlow>
      </div>
    </DoctorLayout>
  );
}

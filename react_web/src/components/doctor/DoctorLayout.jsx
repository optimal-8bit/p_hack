import { Link, useLocation } from 'react-router-dom';
import { Stethoscope, LogOut } from 'lucide-react';
import Aurora from '../ui/Aurora';

export default function DoctorLayout({ children, title, icon: Icon }) {
  const location = useLocation();

  const tabs = [
    { name: 'Dashboard', href: '/doctor-dashboard' },
    { name: 'Appointments', href: '/doctor-appointments' },
    { name: 'Patients', href: '/doctor-patients' },
    { name: 'Prescriptions', href: '/doctor-prescriptions' },
    { name: 'Profile', href: '/doctor-profile' },
  ];

  return (
    <div style={{ position: 'relative', minHeight: '100vh', overflow: 'hidden' }}>
      {/* Aurora Background */}
      <div style={{ position: 'fixed', inset: 0, zIndex: 0 }}>
        <Aurora colorStops={["#7cff67", "#276aff", "#b497cf"]} blend={0.5} amplitude={1.0} speed={0.5} />
      </div>

      {/* Main Container */}
      <div style={{ position: 'relative', zIndex: 10, minHeight: '100vh' }}>
        {/* Top Navigation */}
        <div style={{
          background: 'rgba(18, 15, 23, 0.8)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          padding: '1rem 2rem',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            {/* Logo */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{
                width: 40,
                height: 40,
                borderRadius: 10,
                background: 'linear-gradient(135deg, #7cff67 0%, #276aff 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}>
                <Stethoscope style={{ width: 22, height: 22, color: 'white' }} />
              </div>
            </div>

            {/* Logout Button */}
            <button style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              padding: '8px 16px',
              borderRadius: 8,
              background: 'transparent',
              border: '1px solid rgba(255,255,255,0.1)',
              color: 'rgba(255,255,255,0.8)',
              fontSize: 14,
              fontWeight: 500,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)';
            }}>
              <LogOut style={{ width: 16, height: 16 }} />
              Logout
            </button>
          </div>

          {/* Horizontal Tabs */}
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {tabs.map(tab => {
              const isActive = location.pathname === tab.href;
              return (
                <Link
                  key={tab.name}
                  to={tab.href}
                  style={{
                    padding: '10px 24px',
                    borderRadius: 8,
                    background: isActive ? 'rgba(59, 130, 246, 0.8)' : 'rgba(255,255,255,0.05)',
                    color: isActive ? 'white' : 'rgba(255,255,255,0.7)',
                    fontSize: 14,
                    fontWeight: 500,
                    textDecoration: 'none',
                    transition: 'all 0.2s',
                    border: isActive ? 'none' : '1px solid rgba(255,255,255,0.1)',
                  }}
                >
                  {tab.name}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Page Title */}
        {title && (
          <div style={{ padding: '2rem 2rem 1rem 2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              {Icon && <Icon style={{ width: 24, height: 24, color: 'rgba(255,255,255,0.8)' }} />}
              <h1 style={{ fontSize: 28, fontWeight: 700, color: '#ffffff', margin: 0 }}>{title}</h1>
            </div>
          </div>
        )}

        {/* Page Content */}
        <div style={{ padding: title ? '0 2rem 2rem 2rem' : '2rem' }}>
          {children}
        </div>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

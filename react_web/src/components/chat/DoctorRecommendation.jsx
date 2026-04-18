import { useState, useEffect } from 'react';
import { Stethoscope, AlertCircle, Calendar, X } from 'lucide-react';
import { doctorService } from '@/services/doctor.service';
import MorphingLoader from '../MorphingLoader';

export default function DoctorRecommendation({ recommendation, sessionId }) {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showDoctors, setShowDoctors] = useState(false);
  const [dismissed, setDismissed] = useState(false);

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
                <div style={{ minHeight: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <MorphingLoader 
                    size="md" 
                    color="yellow" 
                    message="Finding specialists..."
                  />
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
                      <div style={{ display: 'flex', gap: 8, fontSize: 12, color: 'rgba(255,255,255,0.6)' }}>
                        {doctor.experience_years > 0 && (
                          <span>{doctor.experience_years} years experience</span>
                        )}
                        {doctor.total_reviews > 0 && (
                          <span>• {doctor.total_reviews} reviews</span>
                        )}
                      </div>
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
  );
}

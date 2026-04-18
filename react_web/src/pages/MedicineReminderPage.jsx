import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Aurora from '../components/ui/Aurora';
import BorderGlow from '../components/ui/BorderGlow';
import ElasticSlider from '../components/ui/ElasticSlider';
import SplitText from '../components/ui/SplitText';

// Sample medicine data with dosesPerDay and dosesTaken
const MEDICINES = [
  { id: 1, name: 'Aspirin', dosage: '100mg', time: '8:00 AM', dosesPerDay: 3, dosesTaken: 2 },
  { id: 2, name: 'Vitamin D', dosage: '1000 IU', time: '12:00 PM', dosesPerDay: 2, dosesTaken: 2 },
  { id: 3, name: 'Metformin', dosage: '500mg', time: '2:00 PM', dosesPerDay: 4, dosesTaken: 1 },
  { id: 4, name: 'Lisinopril', dosage: '10mg', time: '8:00 PM', dosesPerDay: 1, dosesTaken: 0 },
];

export default function MedicineReminderPage() {
  const navigate = useNavigate();
  const [medicines, setMedicines] = useState(MEDICINES);

  const incrementDose = (id) => {
    setMedicines(prev =>
      prev.map(med => 
        med.id === id && med.dosesTaken < med.dosesPerDay
          ? { ...med, dosesTaken: med.dosesTaken + 1 }
          : med
      )
    );
  };

  const decrementDose = (id) => {
    setMedicines(prev =>
      prev.map(med => 
        med.id === id && med.dosesTaken > 0
          ? { ...med, dosesTaken: med.dosesTaken - 1 }
          : med
      )
    );
  };

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      minHeight: '100vh',
      overflow: 'auto',
      background: '#0A0A10',
      fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    }}>
      {/* Aurora Background */}
      <div style={{ position: 'fixed', inset: 0, zIndex: 0 }}>
        <Aurora
          colorStops={["#7cff67", "#276aff", "#b497cf"]}
          blend={0.5}
          amplitude={1.0}
          speed={0.5}
        />
      </div>

      {/* Content */}
      <div style={{
        position: 'relative',
        zIndex: 10,
        padding: '2rem',
        maxWidth: 1200,
        margin: '0 auto',
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '3rem',
        }}>
          <SplitText
            text="Medicine Reminder"
            tag="h1"
            className=""
            delay={40}
            duration={0.6}
            ease="power3.out"
            splitType="chars"
            from={{ opacity: 0, y: 30, scale: 0.9 }}
            to={{ opacity: 1, y: 0, scale: 1 }}
            threshold={0.1}
            rootMargin="0px"
            textAlign="center"
            style={{
              fontSize: 'clamp(2.5rem, 6vw, 4rem)',
              fontWeight: 900,
              color: '#ffffff',
              margin: 0,
              textShadow: '0 4px 20px rgba(0,0,0,0.4), 0 8px 40px rgba(0,0,0,0.3), 0 0 60px rgba(255,255,255,0.2)',
              letterSpacing: '-0.02em',
              filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.3))',
              position: 'relative',
            }}
          />
          <button
            onClick={() => navigate('/chat')}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'rgba(10, 30, 20, 0.92)',
              border: '1px solid rgba(145,241,234,0.3)',
              borderRadius: 12,
              color: '#91f1ea',
              fontSize: 14,
              fontWeight: 700,
              cursor: 'pointer',
              backdropFilter: 'blur(10px)',
              transition: 'all 0.2s',
              textShadow: '0 2px 8px rgba(0,0,0,0.5)',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
            }}
            onMouseEnter={(e) => {
              e.target.style.background = 'rgba(10, 30, 20, 1)';
              e.target.style.transform = 'scale(1.02)';
              e.target.style.borderColor = 'rgba(145,241,234,0.5)';
            }}
            onMouseLeave={(e) => {
              e.target.style.background = 'rgba(10, 30, 20, 0.92)';
              e.target.style.transform = 'scale(1)';
              e.target.style.borderColor = 'rgba(145,241,234,0.3)';
            }}
          >
            Back to Chat
          </button>
        </div>

        {/* Medicine Cards Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '1.5rem',
        }}>
          {medicines.map((medicine) => {
            const progressPercentage = (medicine.dosesTaken / medicine.dosesPerDay) * 100;
            
            return (
              <BorderGlow
                key={medicine.id}
                edgeSensitivity={30}
                glowColor="150 85 50"
                backgroundColor="rgba(10, 30, 20, 0.92)"
                borderRadius={20}
                glowRadius={40}
                glowIntensity={1.2}
                coneSpread={25}
                animated={false}
                colors={['#27f139', '#91f1ea', '#adcf97']}
                fillOpacity={0.4}
              >
                <div style={{ padding: '1.5rem' }}>
                  {/* Header */}
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    marginBottom: '1rem',
                  }}>
                    <div>
                      <h3 style={{
                        fontSize: 22,
                        fontWeight: 700,
                        color: '#91f1ea',
                        margin: '0 0 0.25rem',
                        textShadow: '0 2px 8px rgba(0,0,0,0.5), 0 0 20px rgba(145,241,234,0.3)',
                        letterSpacing: '-0.01em',
                      }}>
                        {medicine.name}
                      </h3>
                      <p style={{
                        fontSize: 14,
                        color: 'rgba(145,241,234,0.7)',
                        margin: 0,
                        fontWeight: 500,
                      }}>
                        {medicine.dosage}
                      </p>
                    </div>
                  </div>

                  {/* Time */}
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    padding: '0.75rem',
                    background: 'rgba(39,241,57,0.1)',
                    border: '1px solid rgba(39,241,57,0.2)',
                    borderRadius: 10,
                    marginBottom: '1rem',
                  }}>
                    <svg viewBox="0 0 24 24" fill="rgba(145,241,234,0.8)" style={{ width: 16, height: 16 }}>
                      <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
                    </svg>
                    <span style={{
                      fontSize: 14,
                      color: 'rgba(145,241,234,0.95)',
                      fontWeight: 600,
                    }}>
                      {medicine.time}
                    </span>
                  </div>

                  {/* Dose Counter */}
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '1rem',
                    padding: '0.75rem',
                    background: 'rgba(39,241,57,0.08)',
                    border: '1px solid rgba(39,241,57,0.15)',
                    borderRadius: 10,
                  }}>
                    <span style={{
                      fontSize: 13,
                      color: 'rgba(145,241,234,0.85)',
                      fontWeight: 600,
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                    }}>
                      Doses Today
                    </span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <button
                        onClick={() => decrementDose(medicine.id)}
                        disabled={medicine.dosesTaken === 0}
                        style={{
                          width: 32,
                          height: 32,
                          borderRadius: '50%',
                          border: '2px solid rgba(145,241,234,0.4)',
                          background: 'rgba(39,241,57,0.15)',
                          color: '#91f1ea',
                          fontSize: 20,
                          fontWeight: 700,
                          cursor: medicine.dosesTaken === 0 ? 'not-allowed' : 'pointer',
                          opacity: medicine.dosesTaken === 0 ? 0.3 : 1,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          transition: 'all 0.2s',
                        }}
                      >
                        −
                      </button>
                      <span style={{
                        fontSize: 18,
                        fontWeight: 700,
                        color: '#91f1ea',
                        minWidth: 70,
                        textAlign: 'center',
                        textShadow: '0 2px 8px rgba(0,0,0,0.4)',
                      }}>
                        {medicine.dosesTaken} / {medicine.dosesPerDay}
                      </span>
                      <button
                        onClick={() => incrementDose(medicine.id)}
                        disabled={medicine.dosesTaken === medicine.dosesPerDay}
                        style={{
                          width: 32,
                          height: 32,
                          borderRadius: '50%',
                          border: '2px solid rgba(145,241,234,0.4)',
                          background: 'rgba(39,241,57,0.15)',
                          color: '#91f1ea',
                          fontSize: 20,
                          fontWeight: 700,
                          cursor: medicine.dosesTaken === medicine.dosesPerDay ? 'not-allowed' : 'pointer',
                          opacity: medicine.dosesTaken === medicine.dosesPerDay ? 0.3 : 1,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          transition: 'all 0.2s',
                        }}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  {/* Progress Slider */}
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '0.5rem',
                    padding: '1rem 0.5rem',
                    background: 'rgba(39,241,57,0.06)',
                    border: '1px solid rgba(39,241,57,0.12)',
                    borderRadius: 10,
                  }}>
                    <span style={{
                      fontSize: 12,
                      color: 'rgba(145,241,234,0.8)',
                      fontWeight: 700,
                      textTransform: 'uppercase',
                      letterSpacing: '0.1em',
                    }}>
                      Progress
                    </span>
                    <ElasticSlider
                      key={`${medicine.id}-${progressPercentage}`}
                      defaultValue={progressPercentage}
                      startingValue={0}
                      maxValue={100}
                      isStepped={false}
                      leftIcon={null}
                      rightIcon={null}
                      readOnly={true}
                    />
                  </div>
                </div>
              </BorderGlow>
            );
          })}
        </div>
      </div>
    </div>
  );
}

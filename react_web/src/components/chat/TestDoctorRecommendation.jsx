import { useState } from 'react';
import DoctorRecommendation from './DoctorRecommendation';

/**
 * TEST COMPONENT - Shows doctor recommendation without backend
 * Use this to verify the UI component works
 */
export default function TestDoctorRecommendation() {
  const [showTest, setShowTest] = useState(false);

  // Test recommendation data
  const testRecommendation = {
    should_recommend: true,
    specialization: "psychologist",
    reason: "Based on what you've shared, speaking with a mental health professional could be beneficial. They can provide personalized support and help you develop strategies to feel better.",
    urgency: "normal"
  };

  const urgentTestRecommendation = {
    should_recommend: true,
    specialization: "psychiatrist", 
    reason: "I'm concerned about your wellbeing. I strongly recommend speaking with a mental health professional who can provide immediate support and guidance.",
    urgency: "urgent"
  };

  return (
    <div style={{ padding: '20px', background: '#1a1a1a', minHeight: '100vh' }}>
      <h2 style={{ color: 'white', marginBottom: '20px' }}>Doctor Recommendation Test</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={() => setShowTest(!showTest)}
          style={{
            padding: '10px 20px',
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            marginRight: '10px'
          }}
        >
          {showTest ? 'Hide' : 'Show'} Normal Recommendation
        </button>
      </div>

      {showTest && (
        <div style={{ marginBottom: '30px' }}>
          <h3 style={{ color: 'white', marginBottom: '10px' }}>Normal Recommendation:</h3>
          <DoctorRecommendation 
            recommendation={testRecommendation}
            sessionId="test-session-123"
          />
        </div>
      )}

      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ color: 'white', marginBottom: '10px' }}>Urgent Recommendation:</h3>
        <DoctorRecommendation 
          recommendation={urgentTestRecommendation}
          sessionId="test-session-456"
        />
      </div>

      <div style={{ 
        background: 'rgba(59, 130, 246, 0.1)', 
        border: '1px solid rgba(59, 130, 246, 0.3)',
        borderRadius: '8px',
        padding: '15px',
        marginTop: '20px'
      }}>
        <h4 style={{ color: '#3b82f6', marginBottom: '10px' }}>Test Instructions:</h4>
        <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px', lineHeight: '1.6' }}>
          1. If you can see the recommendations above, the UI component is working<br/>
          2. Click "Find a Doctor" to test the doctor search functionality<br/>
          3. If this works, the issue is with the backend integration<br/>
          4. Go to: <code>http://localhost:5173/test-doctor-recommendation</code>
        </p>
      </div>
    </div>
  );
}
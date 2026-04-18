import { useState } from 'react'
import { analyzeDiagnosis, imageToBase64 } from '../services/diagnosisService'
import './DiagnosisPage.css'

const AVAILABLE_SYMPTOMS = [
  'itching',
  'redness',
  'fever',
  'cough',
  'fatigue'
]

function DiagnosisPage() {
  const [selectedSymptoms, setSelectedSymptoms] = useState([])
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSymptomToggle = (symptom) => {
    setSelectedSymptoms(prev => {
      if (prev.includes(symptom)) {
        return prev.filter(s => s !== symptom)
      } else {
        return [...prev, symptom]
      }
    })
  }

  const handleImageChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setImageFile(file)
      
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setImagePreview(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleRemoveImage = () => {
    setImageFile(null)
    setImagePreview(null)
  }

  const handleAnalyze = async () => {
    if (selectedSymptoms.length === 0 && !imageFile) {
      setError('Please select at least one symptom or upload an image')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = {
        symptoms: selectedSymptoms
      }

      if (imageFile) {
        const base64Image = await imageToBase64(imageFile)
        data.image_base64 = base64Image
      }

      const response = await analyzeDiagnosis(data)
      setResult(response)
    } catch (err) {
      setError(err.message || 'Failed to analyze. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedSymptoms([])
    setImageFile(null)
    setImagePreview(null)
    setResult(null)
    setError(null)
  }

  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return '#ef4444'
      case 'medium':
        return '#f59e0b'
      case 'low':
        return '#10b981'
      default:
        return '#6b7280'
    }
  }

  return (
    <div className="diagnosis-page">
      <div className="diagnosis-container">
        <header className="diagnosis-header">
          <h1>🏥 Offline AI Health Assistant</h1>
          <p>Upload patient image and select symptoms for instant diagnosis</p>
        </header>

        <div className="diagnosis-content">
          {/* Input Section */}
          <div className="input-section">
            {/* Image Upload */}
            <div className="image-upload-section">
              <h2>Patient Image</h2>
              {!imagePreview ? (
                <label className="image-upload-box">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    style={{ display: 'none' }}
                  />
                  <div className="upload-placeholder">
                    <span className="upload-icon">📷</span>
                    <span>Click to upload image</span>
                    <span className="upload-hint">PNG, JPG up to 10MB</span>
                  </div>
                </label>
              ) : (
                <div className="image-preview-container">
                  <img src={imagePreview} alt="Preview" className="image-preview" />
                  <button
                    onClick={handleRemoveImage}
                    className="remove-image-btn"
                    type="button"
                  >
                    ✕ Remove
                  </button>
                </div>
              )}
            </div>

            {/* Symptom Selection */}
            <div className="symptom-section">
              <h2>Select Symptoms</h2>
              <div className="symptom-grid">
                {AVAILABLE_SYMPTOMS.map(symptom => (
                  <button
                    key={symptom}
                    onClick={() => handleSymptomToggle(symptom)}
                    className={`symptom-btn ${selectedSymptoms.includes(symptom) ? 'selected' : ''}`}
                    type="button"
                  >
                    {selectedSymptoms.includes(symptom) && '✓ '}
                    {symptom}
                  </button>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="action-buttons">
              <button
                onClick={handleAnalyze}
                disabled={loading || (selectedSymptoms.length === 0 && !imageFile)}
                className="analyze-btn"
                type="button"
              >
                {loading ? '🔄 Analyzing...' : '🔍 Analyze'}
              </button>
              <button
                onClick={handleReset}
                disabled={loading}
                className="reset-btn"
                type="button"
              >
                Reset
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
          </div>

          {/* Result Section */}
          {result && (
            <div className="result-section">
              <h2>Diagnosis Result</h2>
              
              <div className="result-card">
                <div className="result-header">
                  <div className="disease-name">
                    {result.disease}
                  </div>
                  <div
                    className="risk-badge"
                    style={{ backgroundColor: getRiskLevelColor(result.risk_level) }}
                  >
                    {result.risk_level} Risk
                  </div>
                </div>

                <div className="confidence-section">
                  <div className="confidence-label">
                    Confidence: {(result.confidence * 100).toFixed(1)}%
                  </div>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{
                        width: `${result.confidence * 100}%`,
                        backgroundColor: getRiskLevelColor(result.risk_level)
                      }}
                    />
                  </div>
                </div>

                <div className="explanation-section">
                  <h3>Explanation</h3>
                  <p>{result.explanation}</p>
                </div>

                {result.all_scores && (
                  <div className="scores-section">
                    <h3>All Disease Probabilities</h3>
                    <div className="scores-list">
                      {Object.entries(result.all_scores)
                        .sort(([, a], [, b]) => b - a)
                        .map(([disease, score]) => (
                          <div key={disease} className="score-item">
                            <span className="score-disease">{disease}</span>
                            <span className="score-value">
                              {(score * 100).toFixed(1)}%
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                )}

                <div className="disclaimer">
                  ⚕️ This is an AI-assisted preliminary assessment. Always consult a healthcare professional for proper medical diagnosis and treatment.
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DiagnosisPage

import { useState } from 'react'
import PropTypes from 'prop-types'
import { X, Upload, FileText, Clock, Pill } from 'lucide-react'
import './PrescriptionModal.css'

export default function PrescriptionModal({ isOpen, onClose, sessionId, onScheduleCreated }) {
  const [step, setStep] = useState(1) // 1: Upload, 2: Review, 3: Schedule
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [medicines, setMedicines] = useState([])
  const [error, setError] = useState(null)

  if (!isOpen) return null

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file')
        return
      }
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        return
      }
      
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setError(null)

    try {
      console.log('Uploading prescription...', { sessionId, fileName: selectedFile.name })
      
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('session_id', sessionId)

      const response = await fetch('http://localhost:8000/api/prescription/upload', {
        method: 'POST',
        body: formData,
      })

      console.log('Upload response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        console.error('Upload failed:', errorData)
        throw new Error(errorData.detail || 'Failed to upload prescription')
      }

      const data = await response.json()
      console.log('Upload successful:', data)
      
      setAnalysisResult(data)
      setMedicines(data.medicines.map(m => ({
        ...m,
        timings: m.timings || ['09:00']
      })))
      console.log('Medicines set:', data.medicines)
      setStep(2)
    } catch (err) {
      console.error('Upload error:', err)
      setError(err.message || 'Failed to upload prescription')
    } finally {
      setIsUploading(false)
    }
  }

  const handleTimingChange = (medicineIndex, timingIndex, value) => {
    const updated = [...medicines]
    updated[medicineIndex].timings[timingIndex] = value
    setMedicines(updated)
  }

  const handleAddTiming = (medicineIndex) => {
    const updated = [...medicines]
    updated[medicineIndex].timings.push('09:00')
    setMedicines(updated)
  }

  const handleRemoveTiming = (medicineIndex, timingIndex) => {
    const updated = [...medicines]
    updated[medicineIndex].timings.splice(timingIndex, 1)
    setMedicines(updated)
  }

  const handleCreateSchedule = async () => {
    setIsUploading(true)
    setError(null)

    try {
      console.log('Creating schedule...', {
        sessionId,
        prescriptionId: analysisResult.prescription_id,
        medicinesCount: medicines.length,
        medicines: medicines
      })

      const response = await fetch(`http://localhost:8000/api/prescription/schedule?session_id=${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prescription_id: analysisResult.prescription_id,
          medicines: medicines,
        }),
      })

      console.log('Schedule response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        console.error('Schedule creation failed:', errorData)
        throw new Error(errorData.detail || 'Failed to create schedule')
      }

      const data = await response.json()
      console.log('Schedule created successfully:', data)
      setStep(3)
      
      // Notify parent component
      if (onScheduleCreated) {
        onScheduleCreated(data)
      }
    } catch (err) {
      console.error('Schedule creation error:', err)
      setError(err.message || 'Failed to create schedule')
    } finally {
      setIsUploading(false)
    }
  }

  const handleClose = () => {
    setStep(1)
    setSelectedFile(null)
    setPreviewUrl(null)
    setAnalysisResult(null)
    setMedicines([])
    setError(null)
    onClose()
  }

  return (
    <div className="prescription-modal-overlay" onClick={handleClose}>
      <div className="prescription-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="prescription-modal-header">
          <h2>
            <Pill size={24} />
            Prescription Analyzer
          </h2>
          <button onClick={handleClose} className="close-button">
            <X size={24} />
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Step 1: Upload */}
        {step === 1 && (
          <div className="prescription-modal-content">
            <div className="upload-section">
              {!selectedFile ? (
                <label className="upload-area">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                  />
                  <Upload size={48} />
                  <p>Click to upload prescription image</p>
                  <span>Supports JPG, PNG (Max 10MB)</span>
                </label>
              ) : (
                <div className="preview-section">
                  <img src={previewUrl} alt="Prescription preview" />
                  <button onClick={() => {
                    setSelectedFile(null)
                    setPreviewUrl(null)
                  }} className="remove-button">
                    Remove
                  </button>
                </div>
              )}
            </div>

            {selectedFile && (
              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="primary-button"
              >
                {isUploading ? 'Analyzing...' : 'Analyze Prescription'}
              </button>
            )}
          </div>
        )}

        {/* Step 2: Review & Schedule */}
        {step === 2 && (
          <div className="prescription-modal-content">
            <div className="analysis-section">
              <h3>
                <FileText size={20} />
                Extracted Medicines
              </h3>
              
              {medicines.map((medicine, mIndex) => (
                <div key={mIndex} className="medicine-card">
                  <div className="medicine-header">
                    <h4>{medicine.medicine_name}</h4>
                    <span className="dosage-badge">{medicine.dosage}</span>
                  </div>
                  
                  <p className="medicine-instructions">{medicine.instructions}</p>
                  
                  <div className="timing-section">
                    <label>
                      <Clock size={16} />
                      Reminder Times
                    </label>
                    
                    {medicine.timings.map((timing, tIndex) => (
                      <div key={tIndex} className="timing-input-group">
                        <input
                          type="time"
                          value={timing}
                          onChange={(e) => handleTimingChange(mIndex, tIndex, e.target.value)}
                          className="timing-input"
                        />
                        {medicine.timings.length > 1 && (
                          <button
                            onClick={() => handleRemoveTiming(mIndex, tIndex)}
                            className="remove-timing-button"
                          >
                            <X size={16} />
                          </button>
                        )}
                      </div>
                    ))}
                    
                    <button
                      onClick={() => handleAddTiming(mIndex)}
                      className="add-timing-button"
                    >
                      + Add Time
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="modal-actions">
              <button onClick={() => setStep(1)} className="secondary-button">
                Back
              </button>
              <button
                onClick={handleCreateSchedule}
                disabled={isUploading}
                className="primary-button"
              >
                {isUploading ? 'Creating...' : 'Create Reminder Schedule'}
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Success */}
        {step === 3 && (
          <div className="prescription-modal-content success-section">
            <div className="success-icon">✓</div>
            <h3>Schedule Created Successfully!</h3>
            <p>Your medicine reminders have been added to the reminder page.</p>
            <button onClick={handleClose} className="primary-button">
              Done
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

PrescriptionModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  sessionId: PropTypes.string.isRequired,
  onScheduleCreated: PropTypes.func,
}

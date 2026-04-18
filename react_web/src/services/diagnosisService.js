import { apiClient } from '../lib/apiClient'

/**
 * Analyze patient symptoms and image for diagnosis
 * @param {Object} data - Diagnosis data
 * @param {string[]} data.symptoms - Array of symptom names
 * @param {string} [data.image_base64] - Optional base64-encoded image
 * @returns {Promise<Object>} Diagnosis result
 */
export async function analyzeDiagnosis(data) {
  return apiClient.post('/health/analyze', data)
}

/**
 * Get diagnosis history
 * @param {number} [limit=10] - Maximum number of records
 * @returns {Promise<Object>} History data
 */
export async function getDiagnosisHistory(limit = 10) {
  return apiClient.get(`/health/history?limit=${limit}`)
}

/**
 * Convert image file to base64
 * @param {File} file - Image file
 * @returns {Promise<string>} Base64-encoded image
 */
export function imageToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

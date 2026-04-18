/**
 * File Type Detection Utility
 * Detects file type based on MIME type and extension
 */

/**
 * Format file size to human-readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} - Formatted size (e.g., "2.5 MB")
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

/**
 * Detect file type category based on MIME type and extension
 * @param {File} file - File object
 * @returns {string} - Human-readable file type category
 */
export const detectFileType = (file) => {
  const mimeType = file.type.toLowerCase()
  const extension = file.name.split('.').pop().toLowerCase()
  
  // PDF Documents
  if (mimeType === 'application/pdf' || extension === 'pdf') {
    return 'PDF Document'
  }
  
  // Images
  if (mimeType.startsWith('image/')) {
    if (extension === 'svg' || mimeType === 'image/svg+xml') {
      return 'SVG Vector'
    }
    return 'Image'
  }
  
  // Videos
  if (mimeType.startsWith('video/')) {
    return 'Video'
  }
  
  // Audio
  if (mimeType.startsWith('audio/')) {
    return 'Audio'
  }
  
  // Word Documents
  if (
    mimeType === 'application/msword' ||
    mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
    extension === 'doc' ||
    extension === 'docx'
  ) {
    return 'Word Document'
  }
  
  // Excel Spreadsheets
  if (
    mimeType === 'application/vnd.ms-excel' ||
    mimeType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
    extension === 'xls' ||
    extension === 'xlsx'
  ) {
    return 'Spreadsheet'
  }
  
  // PowerPoint Presentations
  if (
    mimeType === 'application/vnd.ms-powerpoint' ||
    mimeType === 'application/vnd.openxmlformats-officedocument.presentationml.presentation' ||
    extension === 'ppt' ||
    extension === 'pptx'
  ) {
    return 'Presentation'
  }
  
  // Archives
  if (
    mimeType === 'application/zip' ||
    mimeType === 'application/x-zip-compressed' ||
    mimeType === 'application/x-rar-compressed' ||
    mimeType === 'application/x-rar' ||
    extension === 'zip' ||
    extension === 'rar'
  ) {
    return 'Archive'
  }
  
  // JSON Files
  if (mimeType === 'application/json' || extension === 'json') {
    return 'JSON File'
  }
  
  // XML Files
  if (mimeType === 'application/xml' || mimeType === 'text/xml' || extension === 'xml') {
    return 'XML File'
  }
  
  // Text Files
  if (
    mimeType === 'text/plain' ||
    mimeType === 'text/csv' ||
    extension === 'txt' ||
    extension === 'csv'
  ) {
    if (extension === 'csv') {
      return 'CSV File'
    }
    return 'Text File'
  }
  
  // Unknown
  return 'Unknown File Type'
}

/**
 * Get file information including type and size
 * @param {File} file - File object
 * @returns {Object} - File information
 */
export const getFileInfo = (file) => {
  return {
    name: file.name,
    type: detectFileType(file),
    size: formatFileSize(file.size),
    sizeBytes: file.size,
    mimeType: file.type,
    extension: file.name.split('.').pop().toLowerCase(),
  }
}

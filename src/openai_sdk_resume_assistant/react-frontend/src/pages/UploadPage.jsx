import React, { useState } from 'react';
import { useFileUpload } from '../hooks/useFileUpload';
import '../styles/UploadPage.css';

const UploadPage = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [message, setMessage] = useState('');
  const { upload, uploading, error, uploadResult, reset } = useFileUpload();

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setMessage('');
    reset();
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setMessage('Please select files to upload');
      return;
    }

    setMessage('');

    try {
      const result = await upload(selectedFiles);
      // Create success message with details
      const successMsg = `Successfully uploaded ${result.pdf_count} PDF(s) and ${result.text_count} text file(s)!`;
      
      // Add any errors or warnings if they exist
      if (result.errors && result.errors.length > 0) {
        const errorList = result.errors.join(', ');
        setMessage(`${successMsg}\nWarnings: ${errorList}`);
      } else {
        setMessage(successMsg);
      }
      
      // Clear selected files on success
      setSelectedFiles([]);
      
      // Clear the file input
      const fileInput = document.getElementById('file-input');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (err) {
      setMessage(`Error uploading files: ${err.message}`);
    }
  };

  const handleRemoveFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="upload-page-background">
      <div className="upload-page-container">
        <h1 className="upload-title">Upload Files for Vectorization</h1>
        <p className="upload-description">
          Upload your documents to create vector embeddings for enhanced search and retrieval.
        </p>

        <div className="upload-area">
          <input
            type="file"
            id="file-input"
            className="file-input"
            multiple
            onChange={handleFileSelect}
            accept=".pdf,.txt,.doc,.docx"
          />
          <label htmlFor="file-input" className="file-label">
            <div className="upload-icon">📁</div>
            <span>Click to select files or drag and drop</span>
            <span className="file-types">PDF, TXT, DOC, DOCX</span>
          </label>
        </div>

        {selectedFiles.length > 0 && (
          <div className="selected-files">
            <h3>Selected Files ({selectedFiles.length})</h3>
            <ul className="file-list">
              {selectedFiles.map((file, index) => (
                <li key={index} className="file-item">
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">
                    {(file.size / 1024).toFixed(2)} KB
                  </span>
                  <button
                    className="remove-button"
                    onClick={() => handleRemoveFile(index)}
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={uploading || selectedFiles.length === 0}
        >
          {uploading ? 'Uploading...' : 'Upload Files'}
        </button>

        {message && (
          <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}

        {error && (
          <div className="message error">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
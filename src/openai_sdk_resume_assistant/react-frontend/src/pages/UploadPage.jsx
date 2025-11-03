import React, { useState } from 'react';
import '../styles/UploadPage.css';

const UploadPage = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setMessage('');
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setMessage('Please select files to upload');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      // TODO: Connect to FastAPI backend
      const formData = new FormData();
      selectedFiles.forEach(file => {
        formData.append('files', file);
      });

      // Placeholder for API call
      // const response = await uploadFiles(formData);
      
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate upload
      setMessage('Files uploaded successfully!');
      setSelectedFiles([]);
    } catch (error) {
      setMessage('Error uploading files');
    } finally {
      setUploading(false);
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
      </div>
    </div>
  );
};

export default UploadPage;
import React, { useState } from 'react';
import { useFileUpload } from '../hooks/useFileUpload';
import { useListCollectionItems } from '../hooks/useListCollectionItems';
import '../styles/UploadPage.css';

const UploadPage = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'database'
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const { upload, uploading, error, uploadResult, reset } = useFileUpload();
  const { collectionItems, loading, error: listError, refetch } = useListCollectionItems(refreshTrigger);

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
      setRefreshTrigger(prev => prev + 1); // Trigger refetch of collection items
    } catch (err) {
      setMessage(`Error uploading files: ${err.message}`);
    }
  };

  const handleRemoveFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

//   return (
//     <div className="upload-page-background">
//       <div className="upload-page-container">
//         <h1 className="upload-title">Upload Files for Vectorization</h1>
//         <p className="upload-description">
//           Upload your documents to create vector embeddings for enhanced search and retrieval.
//         </p>

//         <div className="upload-area">
//           <input
//             type="file"
//             id="file-input"
//             className="file-input"
//             multiple
//             onChange={handleFileSelect}
//             accept=".pdf,.txt,.doc,.docx"
//           />
//           <label htmlFor="file-input" className="file-label">
//             <div className="upload-icon">📁</div>
//             <span>Click to select files or drag and drop</span>
//             <span className="file-types">PDF, TXT, DOC, DOCX</span>
//           </label>
//         </div>

//         {selectedFiles.length > 0 && (
//           <div className="selected-files">
//             <h3>Selected Files ({selectedFiles.length})</h3>
//             <ul className="file-list">
//               {selectedFiles.map((file, index) => (
//                 <li key={index} className="file-item">
//                   <span className="file-name">{file.name}</span>
//                   <span className="file-size">
//                     {(file.size / 1024).toFixed(2)} KB
//                   </span>
//                   <button
//                     className="remove-button"
//                     onClick={() => handleRemoveFile(index)}
//                   >
//                     ✕
//                   </button>
//                 </li>
//               ))}
//             </ul>
//           </div>
//         )}

//         <button
//           className="upload-button"
//           onClick={handleUpload}
//           disabled={uploading || selectedFiles.length === 0}
//         >
//           {uploading ? 'Uploading...' : 'Upload Files'}
//         </button>

//         {message && (
//           <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
//             {message}
//           </div>
//         )}

//         {error && (
//           <div className="message error">
//             {error}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

return (
    <div className="upload-page-background">
      <div className="upload-page-container">
        <h1 className="upload-title">Document Management</h1>
        <p className="upload-description">
          Upload and manage your documents for vector search and retrieval.
        </p>

        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            📤 Upload Files
          </button>
          <button
            className={`tab-button ${activeTab === 'database' ? 'active' : ''}`}
            onClick={() => setActiveTab('database')}
          >
            🗄️ Vector Database
          </button>
        </div>

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="tab-content">
            <div className="upload-area">
              <input
                type="file"
                id="file-input"
                className="file-input"
                multiple
                onChange={handleFileSelect}
                accept=".pdf,.txt"
              />
              <label htmlFor="file-input" className="file-label">
                <div className="upload-icon">📁</div>
                <span>Click to select files or drag and drop</span>
                <span className="file-types">PDF, TXT</span>
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
                        disabled={uploading}
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
        )}

        {/* Database Tab */}
        {activeTab === 'database' && (
          <div className="tab-content">
            <div className="database-header">
              <h2>Vector Database Contents</h2>
              <button className="refresh-button" onClick={refetch} disabled={loading}>
                {loading ? '⟳ Loading...' : '🔄 Refresh'}
              </button>
            </div>

            {listError && (
              <div className="message error">
                {listError}
              </div>
            )}

            {loading ? (
              <div className="loading-spinner">Loading collection items...</div>
            ) : collectionItems && collectionItems.exists ? (
              <div className="database-info">
                <div className="stats-container">
                  <div className="stat-card">
                    <div className="stat-value">{collectionItems.files?.length || 0}</div>
                    <div className="stat-label">Total Documents</div>
                  </div>
                </div>

                <div className="files-container">
                  <h3>Files in Database</h3>
                  {collectionItems.files && collectionItems.files.length > 0 ? (
                    <ul className="database-file-list">
                      {collectionItems.files.map((file, index) => (
                        <li key={index} className="database-file-item">
                          <div className="file-icon">📄</div>
                          <div className="file-details">
                            <div className="file-name">{file.name}</div>
                            <div className="file-meta">
                              {file.page_count} chunk{file.page_count !== 1 ? 's' : ''}
                              {file.source && (
                                <span className="file-source"> • {file.source}</span>
                              )}
                            </div>
                          </div>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="empty-state">No files in database yet.</p>
                  )}
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <p>No collection found. Upload files to create one.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
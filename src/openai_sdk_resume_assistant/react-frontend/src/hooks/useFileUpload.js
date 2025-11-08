import { useState } from 'react';
import { uploadFiles } from '../services/api';

export const useFileUpload = () => {
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const [uploadResult, setUploadResult] = useState(null);

    const upload = async (files) => {
        setUploading(true);
        setError(null);
        setUploadResult(null);

        try {
            const result = await uploadFiles(files);
            setUploadResult(result);
            return result;
        } catch (err) {
            const errorMessage = err.response?.data?.detail || err.message || 'Upload failed';
            setError(errorMessage);
            throw new Error(errorMessage);
        } finally {
            setUploading(false);
        }
    };

    const reset = () => {
        setError(null);
        setUploadResult(null);
        setUploading(false);
    };

    return {
        upload,
        uploading,
        error,
        uploadResult,
        reset,
    };
};
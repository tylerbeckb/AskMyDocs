import { useState, useCallback} from 'react';
import {useDropzone, FileWithPath } from 'react-dropzone';
import API from '../app/api/axios';

interface DocumentUploadProps {
    onSuccessfulUpload: () => void;
}

export default function DocumentUpload({ onSuccessfulUpload }: DocumentUploadProps) {
    const [uploading, setUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploadSuccess, setUploadSuccess] = useState(false);

    // Handle file drop
    const onDrop = useCallback(async (acceptedFiles: FileWithPath[]) => {
        const file = acceptedFiles[0];
        // Reset status
        setUploadSuccess(false);

        // Validate file type
        if (!file.name.endsWith('.pdf')) {
            setUploadStatus('Only PDF files are allowed.');
            return;
        }
        setUploading(true);
        setUploadStatus('Uploading...');

        // Prepare form data
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Send file to the server
            const response = await API.post('/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setUploadStatus(`Successfully uploaded ${file.name}, processing document...`);
            setUploadSuccess(true);
            if (onSuccessfulUpload) {
                onSuccessfulUpload();
            }
        } catch (error: any) {
            setUploadStatus(`Error: ${error.response?.data?.detail || 'Failed to upload'}`);
            setUploadSuccess(false);
        } finally {
            setUploading(false);
        }
    }, [onSuccessfulUpload]);

    // Setup dropzone
    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'application/pdf': ['.pdf'] },
        multiple: false,
        disabled: uploading,
    });

    return (
      <div className="w-full max-w-xl mx-auto">
        <div 
          {...getRootProps()} 
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200 ${
            isDragActive 
              ? 'border-blue-500 bg-blue-50' 
              : uploading 
                ? 'border-gray-300 bg-gray-50 cursor-not-allowed' 
                : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center justify-center py-4">
            <svg 
              className={`w-8 h-8 mb-3 ${isDragActive ? 'text-blue-500' : 'text-gray-400'}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24" 
              xmlns="http://www.w3.org/2000/svg"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            {uploading ? (
              <p className="text-gray-600 font-medium">Uploading...</p>
            ) : (
              <>
                <p className="text-gray-700 font-medium mb-1">Drag & drop your travel insurance PDF here</p>
                <p className="text-sm text-gray-500">or click to browse files</p>
              </>
            )}
          </div>
      </div>

      {uploadStatus && (
        <div className={`mt-4 p-4 rounded-lg ${
          uploadSuccess 
            ? 'bg-green-50 border border-green-200 text-green-700' 
            : uploadStatus.startsWith('Error') 
              ? 'bg-red-50 border border-red-200 text-red-700'
              : 'bg-blue-50 border border-blue-200 text-blue-700'
        }`}>
          <div className="flex items-center">
            {uploadSuccess ? (
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            ) : uploadStatus.startsWith('Error') ? (
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            ) : uploading ? (
              <svg className="animate-spin -ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : null}
            <p>{uploadStatus}</p>
          </div>
        </div>
        )}
      </div>
    );
}
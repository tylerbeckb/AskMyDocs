import { useState, useCallback} from 'react';
import {useDropzone, FileWithPath } from 'react-dropzone';
import API from '../app/api/axios';

export default function DocumentUpload() {
    const [uploading, setUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState('');

    // Handle file drop
    const onDrop = useCallback(async (acceptedFiles: FileWithPath[]) => {
        const file = acceptedFiles[0];
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
        } catch (error: any) {
            setUploadStatus(`Error: ${error.response?.data?.detail || 'Failed to upload'}`);
        } finally {
            setUploading(false);
        }
    }, []);

    // Setup dropzone
    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: { 'application/pdf': ['.pdf'] },
        multiple: false,
    });

    return (
        <div className="w-full max-w-xl mx-auto mt-10">
        <div 
          {...getRootProps()} 
          className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center cursor-pointer hover:bg-gray-50"
        >
          <input {...getInputProps()} />
          <p>Drag & drop a PDF here, or click to select</p>
          <p className="text-sm text-gray-500">Only PDF files are accepted</p>
        </div>
        
        {uploadStatus && (
          <div className="mt-4 p-3 bg-gray-100 rounded">
            <p>{uploadStatus}</p>
          </div>
        )}
      </div>
    );
}
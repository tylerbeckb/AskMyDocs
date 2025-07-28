'use client'

import { useState } from 'react';
import DocumentUpload from '@/components/DocumentUpload';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  const [showChat, setShowChat] = useState(false);
  const [hasUploadedDocument, setHasUploadedDocument] = useState(false);

  const handleSuccessfulUpload = () => {
    setHasUploadedDocument(true);
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-gray-800">AskMyDocs</h1>
          </div>
          <div className="text-sm text-gray-500">Travel Insurance Assistant</div>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8">
          <div className="p-6 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              <span className="w-6 h-6 bg-blue-600 rounded-full text-white flex items-center justify-center text-sm">1: Upload your insurance document</span>
            </h2>
          </div>
          <div className="p-6">
            <DocumentUpload onSuccessfulUpload={handleSuccessfulUpload} />
          </div>
        </div>
        
        {hasUploadedDocument && !showChat && (
          <div className="text-center my-8 animate-fadeIn">
            <button
              onClick={() => setShowChat(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-all shadow-md hover:shadow-lg flex items-center mx-auto gap-2"
            >
              <span>Start asking questions</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
              </svg>
            </button>
          </div>
        )}
        
        {showChat && (
          <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8 animate-fadeIn">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-600 rounded-full text-white flex items-center justify-center text-sm">2</span>
                Ask questions about your coverage
              </h2>
            </div>
            <div className="p-6">
              <ChatInterface />
            </div>
          </div>
        )}
      </main>
      
      <footer className="bg-white border-t border-gray-100 py-6 mt-auto">
        <div className="container mx-auto px-4 text-center text-sm text-gray-500">
          © {new Date().getFullYear()} AskMyDocs • AI-powered document assistant
        </div>
      </footer>
    </div>
  );
}
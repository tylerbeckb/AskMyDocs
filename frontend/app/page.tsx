'use client'

import { useState } from 'react';
import DocumentUpload from '@/components/DocumentUpload';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  const [showChat, setShowChat] = useState(false);
  
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8">AskMyDocs - Travel Insurance Assistant</h1>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Step 1: Upload your insurance document</h2>
        <DocumentUpload />
      </div>
      
      <div className="text-center my-8">
        <button
          onClick={() => setShowChat(true)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg"
        >
          Start asking questions
        </button>
      </div>
      
      {showChat && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Step 2: Ask questions about your coverage</h2>
          <ChatInterface />
        </div>
      )}
    </main>
  );
}
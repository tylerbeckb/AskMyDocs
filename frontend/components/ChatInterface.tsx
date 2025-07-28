import { useState, useRef, useEffect } from 'react';
import API from '../app/api/axios';
import ReactMarkdown from 'react-markdown';

type Message = {
    role: 'user' | 'assistant';
    content: string;
    sources?: Array<{source: string; section: string }>;
};

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Scroll to bottom when messages change
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages]);
    
    // Focus input when component mounts
    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    // Handle form submission
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input } as Message;
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);
        
        try {
            const response = await API.post('/api/query', { query: input });
            const assistantMessage = {
                role: 'assistant',
                content: response.data.answer,
                sources: response.data.sources
            } as Message;

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error: any) {
            const errorMessage = {
                role: 'assistant',
                content: `Sorry, I encountered an error: ${error.response?.data?.detail || 'Failed to get a response from the server'}`
            } as Message;
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
            inputRef.current?.focus();
        }
    };

    return (
        <div className="flex flex-col h-[600px] w-full max-w-3xl mx-auto rounded-lg border border-gray-200 overflow-hidden bg-gray-50">
          {/* Chat messages area */}
          <div className="flex-1 overflow-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500 max-w-md">
                  <svg className="w-12 h-12 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                  </svg>
                  <h3 className="font-medium text-gray-900 mb-2">Ask about your travel insurance</h3>
                  <p>Try questions like "What's my coverage for emergency medical care?" or "Are pre-existing conditions covered?"</p>
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
                  <div className={`max-w-[85%] p-4 rounded-lg shadow-sm ${
                    message.role === 'user' 
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white border border-gray-100 rounded-bl-none'
                  }`}>
                    <ReactMarkdown
                      components={{
                        a: ({node, ...props}: any) => (
                          <a {...props} target="_blank" rel="noopener noreferrer" className={`underline ${message.role === 'user' ? 'text-blue-100' : 'text-blue-600'}`} />
                        ),
                        h1: ({node, ...props}: any) => (
                          <h1 {...props} className="text-xl font-bold my-3" />
                        ),
                        h2: ({node, ...props}: any) => (
                          <h2 {...props} className="text-lg font-bold my-2" />
                        ),
                        h3: ({node, ...props}: any) => (
                          <h3 {...props} className="text-md font-semibold my-1" />
                        ),
                        code: ({node, inline, ...props}: any) => (
                          inline 
                            ? <code {...props} className={`px-1 rounded ${message.role === 'user' ? 'bg-blue-500' : 'bg-gray-100'}`} />
                            : <code {...props} className={`block p-2 rounded my-2 overflow-x-auto ${message.role === 'user' ? 'bg-blue-500' : 'bg-gray-100'}`} />
                        ),
                        ul: ({node, ...props}: any) => (
                          <ul {...props} className="list-disc pl-5 my-2 space-y-1" />
                        ),
                        ol: ({node, ...props}: any) => (
                          <ol {...props} className="list-decimal pl-5 my-2 space-y-1" />
                        ),
                        li: ({node, ...props}: any) => (
                          <li {...props} className="my-1" />
                        ),
                        p: ({node, ...props}: any) => (
                          <p {...props} className="my-2" />
                        ),
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                                
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-3 pt-2 border-t border-gray-200 text-xs text-gray-600">
                      <p className="font-semibold mb-1">Sources:</p>
                      <div className="space-y-1">
                        {message.sources.map((source, idx) => (
                          <div key={idx} className="flex items-start">
                            <svg className="w-3 h-3 mt-1 mr-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                              <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd"></path>
                            </svg>
                            <span>{source.source} - {source.section}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
                
          {loading && (
            <div className="flex justify-start animate-fadeIn">
              <div className="bg-white p-4 rounded-lg rounded-bl-none border border-gray-100 shadow-sm">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse delay-150"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse delay-300"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
          </div>
            
        {/* Input area */}
          <div className="border-t border-gray-200 bg-white p-4">
          <form onSubmit={handleSubmit} className="flex items-center space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about your travel insurance..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full disabled:opacity-50 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </form>
        </div>
      </div>
    );
}
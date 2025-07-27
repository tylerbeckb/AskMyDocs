import {useState, useRef, useEffect } from 'react';
import API from '../app/api/axios';
import ReactMarkdown from 'react-markdown';

type Message = {
    role: 'user' | 'assistant';
    content: string;
    sources?: Array<{source: string; section: string }>;
};

// ChatInterface component to handle user input and display messages
export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Handle input change
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    // Effect to scroll to the bottom when messages change
    useEffect(scrollToBottom, [messages]);

    // Handle input change
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input } as Message;
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);
        
        try {
            // Send user input to the server
            const response = await API.post('/api/query', { query: input});
            const assistantMessage = {
                role: 'assistant',
                content: response.data.answer,
                sources: response.data.sources
            } as Message;

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error: any) {
            const errorMessage = {
                role: 'assistant',
                content: `Error: ${error.response?.data?.detail || 'Failed to get response'}`
            } as Message;
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto mt-10 border rounded-lg">
            <div className="flex-1 overflow-auto p-4 space-y-4">
                {messages.map((message, index) => (
                <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] p-3 rounded-lg ${
                    message.role === 'user' 
                        ? 'bg-blue-500 text-white rounded-br-none'
                        : 'bg-gray-200 rounded-bl-none'
                    }`}>
                    <ReactMarkdown
                        components={{
                            // Make links safe by opening in new tab
                            a: ({node, ...props}: any) => (
                                <a {...props} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline" />
                            ),
                            // Style headings appropriately
                            h1: ({node, ...props}: any) => (
                                <h1 {...props} className="text-xl font-bold my-2" />
                            ),
                            h2: ({node, ...props}: any) => (
                                <h2 {...props} className="text-lg font-bold my-1.5" />
                            ),
                            h3: ({node, ...props}: any) => (
                                <h3 {...props} className="text-md font-semibold my-1" />
                            ),
                            // Style code blocks
                            code: ({node, inline, ...props}: any) => (
                                inline 
                                    ? <code {...props} className="bg-gray-100 px-1 rounded" />
                                    : <code {...props} className="block bg-gray-100 p-2 rounded my-2 overflow-x-auto" />
                            ),
                            // Style lists
                            ul: ({node, ...props}: any) => (
                                <ul {...props} className="list-disc pl-5 my-2" />
                            ),
                            ol: ({node, ...props}: any) => (
                                <ol {...props} className="list-decimal pl-5 my-2" />
                            )
                        }}
                    >
                        {message.content}
                    </ReactMarkdown>
                    
                    {message.sources && message.sources.length > 0 && (
                        <div className="mt-2 text-xs border-t pt-1">
                        <p className="font-semibold">Sources:</p>
                        {message.sources.map((source, idx) => (
                            <p key={idx}>{source.source} - {source.section}</p>
                        ))}
                        </div>
                    )}
                    </div>
                </div>
                ))}
                {loading && (
                <div className="flex justify-start">
                    <div className="bg-gray-200 p-3 rounded-lg rounded-bl-none">
                        <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
                        </div>
                    </div>
                </div>
                )}
                <div ref={messagesEndRef} />
            </div>
        
            <form onSubmit={handleSubmit} className="border-t p-4">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about your travel insurance..."
                        className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-blue-500 text-white px-4 py-2 rounded-full disabled:opacity-50"
                    >
                        Send
                    </button>
                </div>
            </form>
        </div>
    )
}
import axios from 'axios';

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:800',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default API;
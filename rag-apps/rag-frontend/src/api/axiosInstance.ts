import axios from 'axios';

const DEFAULT_URL = import.meta.env.VITE_API_URL;
const API_URL = localStorage.getItem('api-url');

const axiosInstance = axios.create({
	baseURL: API_URL ? API_URL : DEFAULT_URL,
	timeout: 100000, // 100 seconds
	headers: {
		Accept: 'application/json'
	}
});

export default axiosInstance;

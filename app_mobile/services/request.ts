import axios from 'axios';
import type { AxiosRequestConfig } from 'axios';
import type { AxiosResponse } from 'axios';

class HttpRequest {
    private baseUrl: string;

    constructor() {
        if (process.env.NODE_ENV === 'production') {
            this.baseUrl = 'https://api.neovisoapp.online/api/';
        }
        else {
            this.baseUrl = 'http://localhost:8080/';
        }

    }

    public async request<T>(method: 'GET' | 'POST' | 'PUT' | 'DELETE', route: string, body?: any): Promise<AxiosResponse<T>> {
        const url = `${this.baseUrl}${route}`;
        const config: AxiosRequestConfig = {
            method,
            url,
            data: body,
        };

        try {
            const response = await axios(config);
            return response;
        } catch (error) {
            throw error;
        }
    }
}

export default HttpRequest;
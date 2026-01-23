const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ApiErrorDetail {
  detail: string | Array<{ loc: string[]; msg: string; type: string }>;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const config: RequestInit = {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const errorBody: ApiErrorDetail = await response.json().catch(() => ({
        detail: 'Something went wrong',
      }));

      // Parsează eroarea - poate fi string sau array
      let message: string;
      if (typeof errorBody.detail === 'string') {
        message = errorBody.detail;
      } else if (Array.isArray(errorBody.detail)) {
        // Format de validare Pydantic
        message = errorBody.detail.map((e) => e.msg).join(', ');
      } else {
        message = 'Something went wrong';
      }

      throw new Error(message);
    }

    const text = await response.text();
    return (text ? JSON.parse(text) : null) as T;
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
export default apiClient;
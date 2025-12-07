import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL + '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add Clerk token to requests if available
api.interceptors.request.use(
  async (config) => {
    if (typeof window !== 'undefined') {
      // Get Clerk session token from window.__clerk
      const clerk = (window as any).__clerk
      if (clerk?.session) {
        try {
          const token = await clerk.session.getToken()
          if (token) {
            config.headers.Authorization = `Bearer ${token}`
          }
        } catch (error) {
          console.error('Failed to get Clerk token:', error)
        }
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle authentication errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('Authentication error:', error.response.data)
    }
    return Promise.reject(error)
  }
)

// Symptom Analysis Types
interface SymptomAnalysisRequest {
  symptoms: string
  age?: number
  gender?: string
  medical_history?: string[]
  duration?: string
  severity?: 'mild' | 'moderate' | 'severe'
}

interface SymptomAnalysisResponse {
  status: string
  safety_check: any
  analysis: any
  recommendations: string[]
  disclaimer: string
  consultation_id?: number
}

// Auth Types
interface RegisterRequest {
  email: string
  password: string
  full_name?: string
}

interface LoginRequest {
  email: string
  password: string
}

interface AuthResponse {
  access_token: string
  token_type: string
  user: any
}

// API Functions

export async function analyzeSymptoms(
  data: SymptomAnalysisRequest
): Promise<SymptomAnalysisResponse> {
  try {
    const response = await api.post('/analyze', data)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Analysis failed')
  }
}

export async function quickEmergencyCheck(symptoms: string) {
  try {
    const response = await api.post('/emergency-check', { symptoms })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Emergency check failed')
  }
}

export async function register(data: RegisterRequest): Promise<AuthResponse> {
  try {
    const response = await api.post('/auth/register', data)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Registration failed')
  }
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
  try {
    const response = await api.post('/auth/login', data)
    // Store token
    localStorage.setItem('token', response.data.access_token)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Login failed')
  }
}

export async function getCurrentUser() {
  try {
    const response = await api.get('/auth/me')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to get user')
  }
}

export async function getConsultationHistory(params?: any) {
  try {
    const response = await api.get('/history', { params })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to get history')
  }
}

export async function getConsultationDetail(id: number) {
  try {
    const response = await api.get(`/history/${id}`)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to get consultation')
  }
}

export async function searchKnowledge(query: string, n_results: number = 5) {
  try {
    const response = await api.get('/knowledge/search', {
      params: { query, n_results }
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Search failed')
  }
}

export async function healthCheck() {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`)
    return response.data
  } catch (error) {
    throw new Error('Health check failed')
  }
}

export function logout() {
  localStorage.removeItem('token')
}

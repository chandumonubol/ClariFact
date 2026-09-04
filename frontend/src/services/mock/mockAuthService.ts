export interface AuthCredentials {
  name: string
  email: string
  password: string
}

export interface AuthUser {
  id: number
  name: string
  email: string
}

export interface AuthResponse {
  user: AuthUser
  access_token: string
  token_type: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export class MockAuthService {
  async register(credentials: AuthCredentials): Promise<AuthResponse> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Mock successful registration
    const user: AuthUser = {
      id: Math.floor(Math.random() * 1000) + 1,
      name: credentials.name,
      email: credentials.email,
    }

    const access_token = `mock-jwt-token-${user.id}`

    return {
      user,
      access_token,
      token_type: 'bearer',
    }
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Mock successful login
    const user: AuthUser = {
      id: 1,
      name: 'Test User',
      email: credentials.email,
    }

    const access_token = `mock-jwt-token-${user.id}`

    return {
      user,
      access_token,
      token_type: 'bearer',
    }
  }

  async getMe(): Promise<AuthUser | null> {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      return JSON.parse(userStr)
    }
    return null
  }

  async logout(): Promise<void> {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }
}

export const mockAuthService = new MockAuthService()
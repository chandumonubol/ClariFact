import { createContext, useContext, useState, useEffect } from 'react'

type AuthContextType = {
  isAuthenticated: boolean
  user: { id: number; name: string; email: string } | null
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
  getMe: () => Promise<{ id: number; name: string; email: string } | null>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<{ id: number; name: string; email: string } | null>(
    null
  )

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const response = await mockAuthService.login({ email, password })
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      setIsAuthenticated(true)
      setUser(response.user)
    } catch (err) {
      throw new Error('Login failed. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (name: string, email: string, password: string) => {
    setIsLoading(true)
    try {
      const response = await mockAuthService.register({ name, email, password })
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      setIsAuthenticated(true)
      setUser(response.user)
    } catch (err) {
      throw new Error('Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    mockAuthService.logout()
    setIsAuthenticated(false)
    setUser(null)
  }

  const getMe = async (): Promise<{ id: number; name: string; email: string } | null> => {
    const user = await mockAuthService.getMe()
    setUser(user)
    setIsAuthenticated(!!user)
    return user
  }

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    setIsAuthenticated(!!token)
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  return (
    <AuthContext
      isAuthenticated={isAuthenticated}
      user={user}
      login={login}
      register={register}
      logout={logout}
      getMe={getMe}
    >
      {children}
    </AuthContext>
  )
}

export { AuthContext }
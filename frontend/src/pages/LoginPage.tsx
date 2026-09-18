import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    if (!email.trim()) {
      setErrors({ email: 'Email is required' })
      return
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setErrors({ email: 'Valid email required' })
      return
    }

    if (!password.trim()) {
      setErrors({ password: 'Password is required' })
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setErrors({ email: data.detail || 'Invalid credentials' })
        setIsLoading(false)
        return
      }

      // Store auth state
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('user', JSON.stringify({ name: data.user.name }))

      navigate('/dashboard')
    } catch (err) {
      setErrors({ email: 'Network error. Please try again.' })
      setIsLoading(false)
    }
  }

  return (
    <section className="min-h-screen bg-bg_light p-8">
      <div className="max-w-md mx-auto space-y-4">
        <h2 className="text-2xl font-bold text-text_primary text-center">Login</h2>

        <form onSubmit={handleSubmit} className="space-y-4 w-full">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              type="email"
              className={`w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent_primary ${errors.email ? 'border-accent_danger' : ''}`}
            />
            {errors.email && <p className="text-accent_danger text-sm mt-1">{errors.email}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••"
              required
              type="password"
              className={`w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent_primary ${errors.password ? 'border-accent_danger' : ''}`}
            />
            {errors.password && <p className="text-accent_danger text-sm mt-1">{errors.password}</p>}
          </div>

          <button type="submit" disabled={isLoading} className={`w-full px-3 py-2 rounded-md ${isLoading ? 'opacity-50 cursor-not-allowed' : 'bg-accent_primary text-white font-medium hover:bg-blue-600 transition-colors'}`}>
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="text-center">
          <p className="text-text_secondary">
            Don't have an account? <Link to="/register" className="font-medium hover:text-accent_primary">Register</Link>
          </p>
        </div>
      </div>
    </section>
  )
}
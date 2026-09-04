import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function RegisterPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    let valid = true

    if (!name.trim()) {
      setErrors((prev) => ({ ...prev, name: 'Name is required' }))
      valid = false
    }

    if (!email.trim()) {
      setErrors((prev) => ({ ...prev, email: 'Email is required' }))
      valid = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setErrors((prev) => ({ ...prev, email: 'Valid email required' }))
      valid = false
    }

    if (!password.trim()) {
      setErrors((prev) => ({ ...prev, password: 'Password is required' }))
      valid = false
    } else if (password.length < 6) {
      setErrors((prev) => ({ ...prev, password: 'Password must be at least 6 characters' }))
      valid = false
    }

    if (!confirmPassword.trim()) {
      setErrors((prev) => ({ ...prev, confirmPassword: 'Confirm password is required' }))
      valid = false
    } else if (password !== confirmPassword) {
      setErrors((prev) => ({ ...prev, confirmPassword: 'Passwords do not match' }))
      valid = false
    }

    if (!valid) return

    setIsLoading(true)
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setErrors({ email: data.detail || 'Registration failed' })
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
        <h2 className="text-2xl font-bold text-text_primary text-center">Create Account</h2>

        <form onSubmit={handleSubmit} className="space-y-4 w-full">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              required
              className={`w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent_primary ${errors.name ? 'border-accent_danger' : ''}`}
            />
            {errors.name && <p className="text-accent_danger text-sm mt-1">{errors.name}</p>}
          </div>

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

          <div>
            <label className="block text-sm font-medium mb-1">Confirm Password</label>
            <input
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••"
              required
              type="password"
              className={`w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent_primary ${errors.confirmPassword ? 'border-accent_danger' : ''}`}
            />
            {errors.confirmPassword && <p className="text-accent_danger text-sm mt-1">{errors.confirmPassword}</p>}
          </div>

          <button type="submit" disabled={isLoading} className={`w-full px-3 py-2 rounded-md ${isLoading ? 'opacity-50 cursor-not-allowed' : 'bg-accent_primary text-white font-medium hover:bg-blue-600 transition-colors'}`}>
            {isLoading ? 'Creating account...' : 'Register'}
          </button>
        </form>

        <div className="text-center">
          <p className="text-text_secondary">
            Already have an account? <Link to="/login" className="font-medium hover:text-accent_primary">Login</Link>
          </p>
        </div>
      </div>
    </section>
  )
}
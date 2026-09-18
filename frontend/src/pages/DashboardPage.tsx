import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

export default function DashboardPage() {
  const [analyses, setAnalyses] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      navigate('/login')
      setIsLoading(false)
      return
    }

    // Fetch analyses from mock endpoint
    const mockAnalyses = [
      {
        id: 1,
        type: 'text',
        content: 'The stock market will crash next month.',
        credibilityScore: 35,
        credibilityLabel: 'Potentially Misleading',
        confidence: 72,
        date: new Date(Date.now() - 86400000).toISOString(),
      },
      {
        id: 2,
        type: 'text',
        content: 'Apple will release a new iPhone in 2024.',
        credibilityScore: 92,
        credibilityLabel: 'Mostly Credible',
        confidence: 95,
        date: new Date(Date.now() - 604800000).toISOString(),
      },
    ]

    setAnalyses(mockAnalyses)
    setIsLoading(false)
  }, [navigate])

  const handleAnalyze = (type: 'text' | 'image' | 'video') => {
    navigate(`/analyze?type=${type}`)
  }

  if (isLoading) {
    return (
      <div className="min-h-[500px] flex items-center justify-center">
        <span className="text-accent_primary">Loading analyses...</span>
      </div>
    )
  }

  return (
    <section className="max-w-7xl mx-auto p-4">
      <header className="mb-6">
        <h2 className="text-3xl font-bold text-text_primary">
          Dashboard
        </h2>
        <p className="text-text_secondary mt-1">
          Welcome to ClariFact
        </p>
      </header>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 mb-6">
        <div className="bg-white rounded-lg p-6 border border-border hover:shadow-md transition-shadow">
          <div className="h-12 w-12 bg-bg_muted rounded-lg flex items-center justify-center">
            <svg className="h-6 w-6 text-accent_primary" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0-2c-2.3 0-4 1.88-4 4s1.69 4 4 4 4-1.88 4-4-1.69-4-4-4zM4 6.72l3.65 3.08L21.76 5c.39-.49.05-.94-.47-.94H5.21l-.36-.27L4 6.72zM5.76 11l5.02 4.25L18.06 15H5.6l-.97-1.08L5.76 11zM5.76 17l5.03 4.25L16.74 21H8.3l-.83-1.04L5.76 17z" />
            </svg>
          </div>
          <h3 className="text-xl font-medium text-text_primary mt-3">Recent Analyses</h3>
          <p className="text-text_secondary mt-1">No analyses yet</p>
          <p className="text-text_secondary mt-2 text-sm">
            Start your first analysis to see results here
          </p>
        </div>

        <div className="bg-white rounded-lg p-6 border border-border hover:shadow-md transition-shadow">
          <div className="h-12 w-12 bg-accent_primary rounded-lg flex items-center justify-center">
            <svg className="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 2c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0-2c-2.3 0-4 1.88-4 4s1.69 4 4 4 4-1.88 4-4-1.69-4-4-4zM4 6.72l3.65 3.08L21.76 5c.39-.49.05-.94-.47-.94H5.21l-.36-.27L4 6.72zM5.76 11l5.02 4.25L18.06 15H5.6l-.97-1.08L5.76 11zM5.76 17l5.03 4.25L16.74 21H8.3l-.83-1.04L5.76 17z" />
            </svg>
          </div>
          <h3 className="text-xl font-medium text-text_primary mt-3">Start New Analysis</h3>
          <div className="mt-4 space-y-3">
            <button
              onClick={() => handleAnalyze('text')}
              className="w-full py-2 bg-accent_primary text-white font-medium rounded-lg hover:bg-blue-600 transition-colors"
            >
              Text Analysis
            </button>
            <button
              onClick={() => handleAnalyze('image')}
              className="w-full py-2 border-2 border-border rounded-lg text-text_primary hover:bg-bg_light transition-colors"
            >
              Image Analysis
            </button>
            <button
              onClick={() => handleAnalyze('video')}
              className="w-full py-2 border-2 border-border rounded-lg text-text_primary hover:bg-bg_light transition-colors"
            >
              Video Analysis
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
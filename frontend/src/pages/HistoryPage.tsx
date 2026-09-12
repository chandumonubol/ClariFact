import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

export default function HistoryPage() {
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

    // In production: fetch('/api/history')
    // For now use mock data
    const mockAnalyses = [
      {
        id: 1,
        type: 'text',
        content: 'The stock market will crash next month.',
        credibilityScore: 35,
        credibilityLabel: 'Potentially Misleading',
        date: new Date(Date.now() - 86400000).toISOString(),
      },
      {
        id: 2,
        type: 'text',
        content: 'Apple will release a new iPhone in 2024.',
        credibilityScore: 92,
        credibilityLabel: 'Mostly Credible',
        date: new Date(Date.now() - 604800000).toISOString(),
      },
    ]

    setAnalyses(mockAnalyses)
    setIsLoading(false)
  }, [navigate])

  if (isLoading) {
    return (
      <div className="min-h-[500px] flex items-center justify-center">
        <span className="text-accent_primary">Loading history...</span>
      </div>
    )
  }

  if (analyses.length === 0) {
    return (
      <section className="p-8 text-center">
        <div className="bg-white rounded-lg p-8 border border-border mb-6">
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-2xl font-bold text-text_primary">No analyses yet</h3>
          <p className="text-text_secondary mb-6">
            Start your first analysis to see your results here.
          </p>
          <button
            onClick={() => navigate('/analyze')}
            className="inline-block px-6 py-3 bg-accent_primary text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Analyze Text
          </button>
        </div>
      </section>
    )
  }

  return (
    <section className="max-w-7xl mx-auto p-4">
      <h3 className="text-2xl font-bold text-text_primary mb-4">
        Analysis History
      </h3>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {analyses.map((analysis) => (
          <div
            key={analysis.id}
            className="bg-white rounded-lg p-4 border border-border hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => navigate(`/analysis/${analysis.id}`)}
          >
            <div className="flex items-center gap-3 mb-2">
              <div
                className={`w-8 h-8 rounded-lg ${analysis.type === 'text' ? 'bg-bg_light' : analysis.type === 'image' ? 'bg-accent_primary' : 'bg-accent_warning'} flex items-center justify-center text-sm`}
              >
                {analysis.type === 'text' ? 'T' : analysis.type === 'image' ? 'I' : 'V'}
              </div>
              <div>
                <p className="font-medium text-text_primary">
                  {analysis.content.substring(0, 40)}{analysis.content.length > 40 ? '...' : ''}
                </p>
                <p className="text-text_secondary text-xs">
                  {new Date(analysis.date).toLocaleDateString()}
                </p>
              </div>
            </div>

            <div className="mt-2">
              <div className="text-xl font-bold">
                {analysis.credibilityScore}/100
              </div>
              <div className="text-sm text-accent_primary">
                {analysis.credibilityLabel}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
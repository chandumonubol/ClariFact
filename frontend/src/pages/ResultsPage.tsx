import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export default function ResultsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      navigate('/login')
      setIsLoading(false)
      return
    }

    // In production: fetch(`/api/analysis/${id}`)
    // For now use mock data
    const mockAnalysis = {
      id: parseInt(id) || 1,
      credibilityScore: 84,
      credibilityLabel: 'Mostly Credible',
      confidence: 88,
      qualityScore: 76,
      claims: [
        {
          id: 1,
          claimText: 'The stock market will crash next month.',
          assessment: 'Partially Supported',
          confidence: 0.72,
          explanation: 'Market timing is notoriously difficult; some indicators suggest volatility but no crash confirmed.',
        },
        {
          id: 2,
          claimText: 'Apple will release a new iPhone in 2024.',
          assessment: 'Supported',
          confidence: 0.95,
          explanation: 'Apple has released new iPhones annually; this aligns with their product cycle.',
        },
      ],
      evidence: [
        {
          sourceName: 'Financial Times',
          snippet: 'Q3 2024 market analysis suggests moderate growth, not crash.'
        },
        {
          sourceName: 'Apple Insider',
          snippet: 'iPhone 16 prototype images leaked, confirming annual release cycle.'
        },
      ],
      explanation:
        'The majority of detected claims are supported by available evidence. One claim could not be sufficiently verified.',
    }

    setAnalysis(mockAnalysis)
    setIsLoading(false)
  }, [id, navigate])

  if (isLoading) {
    return (
      <div className="min-h-[500px] flex items-center justify-center">
        <span className="text-accent_primary">Loading analysis...</span>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="text-center py-8">
        <p className="text-text_secondary">No analysis found.</p>
        <button
          onClick={() => navigate('/history')}
          className="mt-4 inline-block px-4 py-2 bg-accent_primary text-white rounded-hover text-sm"
        >
          Go to History
        </button>
      </div>
    )
  }

  const labelClass = {
    'Mostly Credible': 'text-accent_primary',
    'Partially Supported': 'text-accent_warning',
    'Uncertain': 'text-text_secondary',
    'Potentially Misleading': 'text-accent_danger',
  }[analysis.credibilityLabel] || 'text-text_secondary'

  return (
    <section className="max-w-3xl mx-auto p-4">
      <div className="bg-white rounded-lg p-6 border border-border">
        <div className="mb-6">
          <div className="text-4xl font-bold">{analysis.credibilityScore}/100</div>
          <div className={`text-{labelClass} mt-2 font-medium`}>
            {analysis.credibilityLabel}
          </div>
          <div className="mt-3">
            <div className="text-sm text-text_secondary">Confidence</div>
            <div className="w-full bg-bg_muted rounded-hl lg:rounded-3xl h-2 lg:h-2.5 mt-1">
              <div
                className={`h-full rounded-hl lg:rounded-3xl bg-accent_primary ${analysis.confidence > 50 ? 'bg-accent_secondary' : ''} transition-colors`}
                style={{ width: `${analysis.confidence}%` }}
              ></div>
            </div>
            <span className="text-xs text-text_secondary ml-2">{analysis.confidence}%</span>
          </div>
        </div>

        <div className="mb-4">
          <h4 className="text-lg font-medium text-text_primary mb-2">
            Assessment
          </h4>
          <p className="text-text_secondary">{analysis.explanation}</p>
        </div>

        <div className="mb-4">
          <h4 className="text-lg font-medium text-text_primary mb-2">
            Claims Detected
          </h4>
          {analysis.claims.map((claim: any) => {
            const assessmentClass = {
              Supported: 'text-accent_primary',
              'Partially Supported': 'text-accent_warning',
              Uncertain: 'text-text_secondary',
              'Potentially Misleading': 'text-accent_danger',
            }[claim.assessment] || 'text-text_secondary'

            return (
              <div className="flex items-center gap-2 mb-2">
                <span className={`w-2 h-2 rounded-full ${assessmentClass}`} />
                <span className="font-medium">{claim.claimText}</span>
                <span className={`text-sm font-medium ${assessmentClass}`}>
                  {claim.assessment}
                </span>
              </div>
            )
          })}
        </div>

        <div className="mb-4">
          <h4 className="text-lg font-medium text-text_primary mb-2">
            Evidence / Sources
          </h4>
          {analysis.evidence.map((source: any, index: number) => (
            <div key={index} className="p-3 bg-bg_muted rounded-md mb-2">
              <a
                href="#"
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent_primary hover underline text-sm"
              >
                {source.sourceName}
              </a>
              <p className="text-text_secondary text-xs mt-1">
                {source.snippet}
              </p>
            </div>
          ))}

          {analysis.evidence.length === 0 && (
            <p className="text-text_secondary text-xs mt-2">
              No evidence sources available
            </p>
          )}
        </div>

        <div className="mt-6 pt-6 border-t border-border">
          <p className="text-text_secondary text-sm">
            AI-assisted credibility assessment. Score based on available evidence.
          </p>
        </div>
      </div>
    </section>
  )
}
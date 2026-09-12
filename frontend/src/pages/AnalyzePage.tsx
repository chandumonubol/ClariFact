import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

export default function AnalyzePage() {
  const [text, setText] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const urlParams = new URLSearchParams(location.search)
  const type = urlParams.get('type') || 'text'

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    if (!text.trim()) {
      setErrors({ text: 'Please enter content to analyze' })
      return
    }

    if (text.trim().length < 10) {
      setErrors({ text: 'Text is too short (minimum 10 characters)' })
      return
    }

    setIsSubmitting(true)
    try {
      setIsProcessing(true)

      // Mock analysis service - in production this would POST to /api/analyze
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Navigate to results with mock analysis ID
      const mockAnalysisId = Math.floor(Math.random() * 1000) + 1
      navigate(`/results/${mockAnalysisId}`)
    } catch (err) {
      setErrors({ text: 'Analysis failed. Please try again.' })
    } finally {
      setIsSubmitting(false)
      setIsProcessing(false)
    }
  }

  return (
    <section className="max-w-2xl mx-auto p-4">
      <header className="mb-6">
        <h2 className="text-2xl font-bold text-text_primary">
          {type === 'text' ? 'Text Analysis' : type === 'image' ? 'Image Analysis' : 'Video Analysis'}
        </h2>
        <p className="text-text_secondary mt-1">
          Enter the content you want ClariFact to assess
        </p>
      </header>

      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste the content you want ClariFact to assess..."
          rows={4}
          required
          disabled={isSubmitting || isProcessing}
          className={`w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-accent_primary ${errors.text ? 'border-accent_danger' : ''} resize-none min-h-[120px]`}
        />
        {errors.text && <p className="text-accent_danger text-sm mt-1">{errors.text}</p>}

        <div>
          <button type="submit" disabled={isSubmitting || isProcessing} className={`w-full py-2 rounded-md ${isSubmitting || isProcessing ? 'opacity-50 cursor-not-allowed' : 'bg-accent_primary text-white font-medium hover:bg-blue-600 transition-colors'}`}>
            {isProcessing ? 'Analyzing...' : isSubmitting ? 'Submitting...' : 'Analyze'}
          </button>
        </div>
      </form>
    </section>
  )
}
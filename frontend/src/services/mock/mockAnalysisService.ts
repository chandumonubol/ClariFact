import { AnalysisRequest, AnalysisResponse, AnalysisSummary } from './analysisService'

const MOCK_ANALYSES: AnalysisSummary[] = [
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

const MOCK_ANALYSIS_RESPONSE: AnalysisResponse = {
  overall_credibility_score: 84,
  credibility_label: 'Mostly Credible',
  confidence: 88,
  quality_score: 76,
  claims: [
    {
      id: 1,
      claim_text: 'The stock market will crash next month.',
      assessment: 'Partially Supported',
      confidence: 0.72,
      explanation: 'Market timing is notoriously difficult; some indicators suggest volatility but no crash confirmed.',
    },
    {
      id: 2,
      claim_text: 'Apple will release a new iPhone in 2024.',
      assessment: 'Supported',
      confidence: 0.95,
      explanation: 'Apple has released new iPhones annually; this aligns with their product cycle.',
    },
  ],
  evidence: [
    {
      source_name: 'Financial Times',
      snippet: 'Q3 2024 market analysis suggests moderate growth, not crash.'
    },
    {
      source_name: 'Apple Insider',
      snippet: 'iPhone 16 prototype images leaked, confirming annual release cycle.'
    },
  ],
  explanation:
    'The majority of detected claims are supported by available evidence. One claim could not be sufficiently verified.',
}

export class MockAnalysisService {
  async submitText(text: string): Promise<AnalysisResponse> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Return mock analysis result
    return MOCK_ANALYSIS_RESPONSE
  }

  async getHistory(): Promise<AnalysisSummary[]> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000))
    return MOCK_ANALYSES
  }

  async getAnalysis(id: number): Promise<AnalysisResponse> {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000))
    return MOCK_ANALYSIS_RESPONSE
  }
}

export const mockAnalysisService = new MockAnalysisService()
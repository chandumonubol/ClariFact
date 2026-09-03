export interface AnalysisRequest {
  content_type: 'text' | 'image' | 'video'
  text_content?: string
  file_path?: string
}

export interface Claim {
  id: number
  claim_text: string
  assessment: 'Supported' | 'Partially Supported' | 'Uncertain' | 'Potentially Misleading'
  confidence: number
  explanation: string
}

export interface Evidence {
  source_name: string
  snippet: string
}

export interface AnalysisResponse {
  overall_credibility_score: number
  credibility_label: string
  confidence: number
  quality_score: number
  claims: Claim[]
  evidence: Evidence[]
  explanation: string
}

export interface AnalysisSummary {
  id: number
  type: 'text' | 'image' | 'video'
  content: string
  credibilityScore: number
  credibilityLabel: string
  confidence: number
  date: string
}
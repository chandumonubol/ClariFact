import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import HistoryPage from '../pages/HistoryPage'
import ResultsPage from '../pages/ResultsPage'

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  localStorage.clear()
})

describe('History Page', () => {
  it('renders the history page', () => {
    render(<HistoryPage />)
    const title = screen.getByRole('heading', { name: /analysis history/i })
    expect(title).toBeInTheDocument()
  })

  it('shows empty state when no analyses', () => {
    render(<HistoryPage />)
    const emptyState = screen.getByText('No analyses yet')
    expect(emptyState).toBeInTheDocument()
  })

  it('shows analysis cards when analyses exist', () => {
    // Mock analyses in localStorage
    localStorage.setItem(
      'analyses',
      JSON.stringify([
        {
          id: 1,
          type: 'text',
          content: 'Test content',
          credibilityScore: 84,
          credibilityLabel: 'Mostly Credible',
          date: new Date().toISOString(),
        },
      ])
    )

    render(<HistoryPage />)
    const cards = screen.getByTestId('analysis-card')
    expect(cards.length).toBe(1)
  })
})

describe('Results Page', () => {
  it('renders the results page', () => {
    render(<ResultsPage />)
    const heading = screen.getByRole('heading', { name: /credibility/i })
    expect(heading).toBeInTheDocument()
  })

  it('shows empty state when no analysis found', () => {
    render(<ResultsPage />)
    const notFound = screen.getByText('No analysis found')
    expect(notFound).toBeInTheDocument()
  })
})
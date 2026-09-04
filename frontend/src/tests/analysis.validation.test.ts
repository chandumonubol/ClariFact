import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AnalyzePage from '../pages/AnalyzePage'

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  localStorage.clear()
})

describe('Text Analysis', () => {
  it('renders the analysis form', () => {
    render(<AnalyzePage />)
    const title = screen.getByRole('heading', { name: /text analysis/i })
    expect(title).toBeInTheDocument()
  })

  it('shows error when text is empty', async () => {
    const user = userEvent.setup()
    render(<AnalyzePage />)

    await user.click(screen.getByRole('button', { name: /analyze/i }))

    expect(screen.getByText('Please enter content to analyze')).toBeInTheDocument()
  })

  it('shows error when text is too short', async () => {
    const user = userEvent.setup()
    render(<AnalyzePage />)

    await user.type(screen.getByTagName('textarea')[0], 'short')
    await user.click(screen.getByRole('button', { name: /analyze/i }))

    expect(screen.getByText('Text is too short (minimum 10 characters)')).toBeInTheDocument()
  })

  it('submits text for analysis', async () => {
    const user = userEvent.setup()
    render(<AnalyzePage />)

    await user.type(screen.getByTagName('textarea')[0], 'The stock market will crash next month. This is a test content that is long enough to pass validation.')
    await user.click(screen.getByRole('button', { name: /analyze/i }))

    // After submission, should navigate to results
    const token = localStorage.getItem('access_token')
    expect(token).toBeTruthy()
  })
})
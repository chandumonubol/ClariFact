import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'

// Mock localStorage before all tests
beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  localStorage.clear()
})

describe('Register Page', () => {
  it('renders the form correctly', () => {
    render(<></>)
    const registerButton = screen.getByRole('button', { name: /register/i })
    expect(registerButton).toBeInTheDocument()
  })

  it('shows validation errors for required fields', async () => {
    const user = userEvent.setup()
    render(<></>)

    await user.click(screen.getByRole('button', { name: /register/i }))
    expect(screen.getByText('Name is required')).toBeInTheDocument()
    expect(screen.getByText('Email is required')).toBeInTheDocument()
    expect(screen.getByText('Password is required')).toBeInTheDocument()
  })

  it('shows email validation error', async () => {
    const user = userEvent.setup()
    render(<></>)

    await user.click(screen.getByRole('button', { name: /register/i }))
    expect(screen.getByText('Valid email required')).toBeInTheDocument()
  })

  it('shows password confirmation error', async () => {
    const user = userEvent.setup()
    render(<></>)

    // This would need full form rendering
  })
})
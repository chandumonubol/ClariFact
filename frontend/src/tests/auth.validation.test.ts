import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RegisterPage from '../pages/RegisterPage'
import LoginPage from '../pages/LoginPage'

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  localStorage.clear()
})

describe('Register Page', () => {
  it('renders the register form', () => {
    render(<RegisterPage />)
    const title = screen.getByRole('heading', { name: /create account/i })
    expect(title).toBeInTheDocument()
  })

  it('shows name validation error when empty', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)

    await user.type(screen.getByLabelText('Name'), '')
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.type(screen.getByLabelText('Confirm Password'), 'password123')
    await user.click(screen.getByRole('button', { name: /register/i }))

    expect(screen.getByText('Name is required')).toBeInTheDocument()
  })

  it('shows email validation error for invalid email', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)

    await user.type(screen.getByLabelText('Name'), 'Test User')
    await user.type(screen.getByLabelText('Email'), 'invalid-email')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.type(screen.getByLabelText('Confirm Password'), 'password123')
    await user.click(screen.getByRole('button', { name: /register/i }))

    expect(screen.getByText('Valid email required')).toBeInTheDocument()
  })

  it('shows password too short error', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)

    await user.type(screen.getByLabelText('Name'), 'Test User')
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Password'), 'short')
    await user.type(screen.getByLabelText('Confirm Password'), 'short')
    await user.click(screen.getByRole('button', { name: /register/i }))

    expect(screen.getByText('Password must be at least 6 characters')).toBeInTheDocument()
  })

  it('shows password mismatch error', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)

    await user.type(screen.getByLabelText('Name'), 'Test User')
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.type(screen.getByLabelText('Confirm Password'), 'differentpassword')
    await user.click(screen.getByRole('button', { name: /register/i }))

    expect(screen.getByText('Passwords do not match')).toBeInTheDocument()
  })

  it('submits successfully with valid data', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)

    await user.type(screen.getByLabelText('Name'), 'Test User')
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.type(screen.getByLabelText('Confirm Password'), 'password123')
    await user.click(screen.getByRole('button', { name: /register/i }))

    // After successful register, should navigate to dashboard
    // Check that localStorage was set
    const token = localStorage.getItem('access_token')
    expect(token).toBeTruthy()
  })
})

describe('Login Page', () => {
  it('renders the login form', () => {
    render(<LoginPage />)
    const title = screen.getByRole('heading', { name: /login/i })
    expect(title).toBeInTheDocument()
  })

  it('shows email validation error when empty', async () => {
    const user = userEvent.setup()
    render(<LoginPage />)

    await user.click(screen.getByRole('button', { name: /login/i }))

    expect(screen.getByText('Email is required')).toBeInTheDocument()
  })

  it('shows password validation error when empty', async () => {
    const user = userEvent.setup()
    render(<LoginPage />)

    await user.click(screen.getByRole('button', { name: /login/i }))

    expect(screen.getByText('Password is required')).toBeInTheDocument()
  })

  it('shows invalid credentials error', async () => {
    const user = userEvent.setup()
    render(<LoginPage />)

    await user.type(screen.getByLabelText('Email'), 'nonexistent@example.com')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.click(screen.getByRole('button', { name: /login/i }))

    expect(screen.getByText('Invalid credentials')).toBeInTheDocument()
  })

  it('submits successfully with valid credentials', async () => {
    const user = userEvent.setup()
    render(<LoginPage />)

    // Set mock user first via register, then login
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.click(screen.getByRole('button', { name: /login/i }))

    // After successful login, token should be stored
    const token = localStorage.getItem('access_token')
    expect(token).toBeTruthy()
  })
})
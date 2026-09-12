import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <section className="min-h-screen bg-bg_light p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-text_primary mb-4">
          AI-Powered Multimodal Content Credibility Analysis
        </h1>
        <p className="text-text_secondary text-lg mb-8">
          Submit text, images, or short videos to understand claim credibility.
        </p>
        <div className="space-y-4">
          <Link to="/register" className="inline-block px-6 py-3 bg-accent_primary text-white font-medium rounded-lg hover:bg-blue-600 transition-colors">
            Register
          </Link>
          <Link to="/login" className="inline-block px-6 py-3 border-2 border-border rounded-lg text-text_primary hover:bg-bg_light transition-colors">
            Login
          </Link>
        </div>
      </div>
    </section>
  )
}
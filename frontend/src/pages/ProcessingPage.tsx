export default function ProcessingPage() {
  return (
    <section className="min-h-screen flex items-center justify-center p-8">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-bg_muted mb-4">
          <svg className="w-8 h-8 text-accent_primary" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10" />
            <path
              d="M12 6v6l4 2"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>

        <h3 className="text-2xl font-bold text-text_primary">
          Analyzing your content
        </h3>
        <p className="text-text_secondary mt-2">
          Extracting claims, checking evidence, assessing credibility
        </p>
      </div>
    </section>
  )
}
export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">HealthSentiment</h3>
            <p className="text-sm text-gray-600">
              Advanced AI-powered sentiment analysis for healthcare reviews and patient feedback.
            </p>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 mb-3">Features</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>Real-time sentiment analysis</li>
              <li>Batch processing capabilities</li>
              <li>Healthcare-specific model</li>
              <li>Export and reporting tools</li>
            </ul>
          </div>

          <div>
            <h4 className="font-medium text-gray-900 mb-3">Technology</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>Machine Learning Classification</li>
              <li>TF-IDF Vectorization</li>
              <li>RESTful API Architecture</li>
              <li>Responsive Web Design</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 mt-8 pt-6 text-center">
          <p className="text-sm text-gray-500">
            © 2024 HealthSentiment. Built with Next.js, Flask, and Machine Learning.
          </p>
        </div>
      </div>
    </footer>
  )
}

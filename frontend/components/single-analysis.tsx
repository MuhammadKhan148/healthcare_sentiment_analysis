"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2, Send, ThumbsUp, ThumbsDown, Minus } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { getApiUrl } from "@/lib/config"

interface AnalysisResult {
  text: string
  sentiment: "positive" | "negative" | "neutral"
  confidence: number
  timestamp: string
  model_used?: string
}

export function SingleAnalysis() {
  const [text, setText] = useState("")
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError("Please enter some text to analyze")
      return
    }

    setLoading(true)
    setError("")
    setResult(null)

    try {
      const response = await fetch(getApiUrl('/api/analyze'), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text.trim() }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Analysis failed")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error('Error analyzing sentiment:', err)
      setError(err instanceof Error ? err.message : "An error occurred while analyzing sentiment")
    } finally {
      setLoading(false)
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-green-50 text-green-700 border-green-200"
      case "negative":
        return "bg-red-50 text-red-700 border-red-200"
      case "neutral":
        return "bg-gray-50 text-gray-700 border-gray-200"
      default:
        return "bg-gray-50 text-gray-700 border-gray-200"
    }
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return <ThumbsUp className="w-4 h-4" />
      case "negative":
        return <ThumbsDown className="w-4 h-4" />
      case "neutral":
        return <Minus className="w-4 h-4" />
      default:
        return <Minus className="w-4 h-4" />
    }
  }

  const getConfidenceColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-green-500"
      case "negative":
        return "bg-red-500"
      case "neutral":
        return "bg-gray-500"
      default:
        return "bg-gray-500"
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Single Review Analysis</CardTitle>
          <CardDescription>
            Enter a healthcare review to analyze its sentiment
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder="Enter your healthcare review here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="min-h-[120px]"
          />
          <Button 
            onClick={analyzeSentiment} 
            disabled={loading || !text.trim()}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Analyze Sentiment
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>
            {error}
            <br />
            <span className="text-sm">Make sure the Flask API is running on port 5328</span>
          </AlertDescription>
        </Alert>
      )}

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-gray-900">Review Text</h4>
              <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded-md">
                {result.text}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">Sentiment</h4>
                <Badge className={`${getSentimentColor(result.sentiment)} flex items-center space-x-1 w-fit`}>
                  {getSentimentIcon(result.sentiment)}
                  <span className="capitalize">{result.sentiment}</span>
                </Badge>
              </div>

              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">Confidence</h4>
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getConfidenceColor(result.sentiment)}`}
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium">
                    {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>

            {result.model_used && (
              <div className="text-xs text-gray-500">
                Model used: {result.model_used}
              </div>
            )}

            <div className="text-xs text-gray-500">
              Analyzed at: {new Date(result.timestamp).toLocaleString()}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

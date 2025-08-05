"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Upload, Download, FileText, Loader2, BarChart3 } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface BatchResult {
  id: number
  text: string
  sentiment: "positive" | "negative" | "neutral"
  confidence: number
}

interface BatchAnalysisResult {
  results: BatchResult[]
  summary: {
    total: number
    positive: number
    negative: number
    neutral: number
  }
  timestamp: string
}

export function BatchAnalysis() {
  const [file, setFile] = useState<File | null>(null)
  const [results, setResults] = useState<BatchAnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [uploadProgress, setUploadProgress] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile) {
      if (selectedFile.type !== "text/csv" && !selectedFile.name.endsWith(".csv")) {
        setError("Please select a CSV file")
        return
      }
      setFile(selectedFile)
      setError("")
    }
  }

  const analyzeBatch = async () => {
    if (!file) {
      setError("Please select a CSV file")
      return
    }

    setLoading(true)
    setError("")
    setUploadProgress(0)

    const formData = new FormData()
    formData.append("file", file)

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      const response = await fetch("/api/analyze-batch", {
        method: "POST",
        body: formData,
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Batch analysis failed")
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setLoading(false)
      setTimeout(() => setUploadProgress(0), 1000)
    }
  }

  const downloadResults = () => {
    if (!results) return

    const csvContent = [
      ["ID", "Text", "Sentiment", "Confidence"],
      ...results.results.map((r) => [
        r.id.toString(),
        `"${r.text.replace(/"/g, '""')}"`,
        r.sentiment,
        r.confidence.toString(),
      ]),
    ]
      .map((row) => row.join(","))
      .join("\n")

    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `sentiment_analysis_results_${new Date().toISOString().split("T")[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-green-50 text-green-700"
      case "negative":
        return "bg-red-50 text-red-700"
      case "neutral":
        return "bg-gray-50 text-gray-700"
      default:
        return "bg-gray-50 text-gray-700"
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Batch Analysis</CardTitle>
          <CardDescription>Upload a CSV file with healthcare reviews for bulk sentiment analysis</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <input type="file" accept=".csv" onChange={handleFileSelect} ref={fileInputRef} className="hidden" />

            {file ? (
              <div className="space-y-2">
                <FileText className="w-8 h-8 text-gray-600 mx-auto" />
                <p className="text-sm font-medium">{file.name}</p>
                <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
                <Button variant="outline" size="sm" onClick={() => fileInputRef.current?.click()}>
                  Change File
                </Button>
              </div>
            ) : (
              <div className="space-y-2">
                <Upload className="w-8 h-8 text-gray-400 mx-auto" />
                <p className="text-sm text-gray-600">Click to upload or drag and drop your CSV file</p>
                <p className="text-xs text-gray-500">
                  CSV file should contain a 'text', 'review', 'comment', or 'feedback' column
                </p>
                <Button variant="outline" onClick={() => fileInputRef.current?.click()}>
                  Select File
                </Button>
              </div>
            )}
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {loading && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Processing...</span>
                <span>{uploadProgress}%</span>
              </div>
              <Progress value={uploadProgress} className="w-full" />
            </div>
          )}

          <Button onClick={analyzeBatch} disabled={loading || !file} className="w-full sm:w-auto">
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <BarChart3 className="w-4 h-4 mr-2" />
                Analyze Batch
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {results && (
        <>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Analysis Summary</CardTitle>
                <CardDescription>Results from {results.summary.total} reviews</CardDescription>
              </div>
              <Button onClick={downloadResults} variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Export CSV
              </Button>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900">{results.summary.total}</div>
                  <div className="text-sm text-gray-600">Total Reviews</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{results.summary.positive}</div>
                  <div className="text-sm text-gray-600">Positive</div>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <div className="text-2xl font-bold text-red-600">{results.summary.negative}</div>
                  <div className="text-sm text-gray-600">Negative</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-gray-600">{results.summary.neutral}</div>
                  <div className="text-sm text-gray-600">Neutral</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Detailed Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-16">ID</TableHead>
                      <TableHead>Review Text</TableHead>
                      <TableHead className="w-24">Sentiment</TableHead>
                      <TableHead className="w-24">Confidence</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {results.results.slice(0, 10).map((result) => (
                      <TableRow key={result.id}>
                        <TableCell className="font-medium">{result.id}</TableCell>
                        <TableCell className="max-w-md">
                          <div className="truncate" title={result.text}>
                            {result.text}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge className={getSentimentColor(result.sentiment)}>{result.sentiment}</Badge>
                        </TableCell>
                        <TableCell>{(result.confidence * 100).toFixed(1)}%</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
              {results.results.length > 10 && (
                <div className="mt-4 text-center text-sm text-gray-500">
                  Showing first 10 results. Download CSV for complete data.
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}

"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Target, TrendingUp, Activity, Zap } from "lucide-react"
import { getApiUrl } from "@/lib/config"

interface ModelMetrics {
  accuracy: number
  precision: number
  recall: number
  f1_score: number
  last_updated: string
  training_samples?: number
  testing_samples?: number
  total_samples?: number
}

export function ModelMetrics() {
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    fetchMetrics()
  }, [])

  const fetchMetrics = async () => {
    try {
      const response = await fetch(getApiUrl('/api/metrics'), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setMetrics(data)
    } catch (err) {
      console.error('Error fetching metrics:', err)
      setError(err instanceof Error ? err.message : "An error occurred while fetching metrics")
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.9) return "text-green-600"
    if (score >= 0.8) return "text-yellow-600"
    return "text-red-600"
  }

  const getScoreBadge = (score: number) => {
    if (score >= 0.9) return "bg-green-50 text-green-700"
    if (score >= 0.8) return "bg-yellow-50 text-yellow-700"
    return "bg-red-50 text-red-700"
  }

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-600 mx-auto mb-2"></div>
            <p className="text-sm text-gray-600">Loading model metrics...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>
          {error}
          <br />
          <span className="text-sm">Make sure the Flask API is running on port 5328</span>
        </AlertDescription>
      </Alert>
    )
  }

  if (!metrics) return null

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Target className="w-5 h-5" />
            <span>Model Performance Metrics</span>
          </CardTitle>
          <CardDescription>Current performance metrics of the healthcare sentiment analysis model</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">Accuracy</span>
                <Badge className={getScoreBadge(metrics.accuracy)}>{(metrics.accuracy * 100).toFixed(1)}%</Badge>
              </div>
              <Progress value={metrics.accuracy * 100} className="h-2" />
              <p className="text-xs text-gray-500">Overall correctness of predictions</p>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">Precision</span>
                <Badge className={getScoreBadge(metrics.precision)}>{(metrics.precision * 100).toFixed(1)}%</Badge>
              </div>
              <Progress value={metrics.precision * 100} className="h-2" />
              <p className="text-xs text-gray-500">Accuracy of positive predictions</p>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">Recall</span>
                <Badge className={getScoreBadge(metrics.recall)}>{(metrics.recall * 100).toFixed(1)}%</Badge>
              </div>
              <Progress value={metrics.recall * 100} className="h-2" />
              <p className="text-xs text-gray-500">Ability to find all positive cases</p>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">F1 Score</span>
                <Badge className={getScoreBadge(metrics.f1_score)}>{(metrics.f1_score * 100).toFixed(1)}%</Badge>
              </div>
              <Progress value={metrics.f1_score * 100} className="h-2" />
              <p className="text-xs text-gray-500">Harmonic mean of precision and recall</p>
            </div>
          </div>

          {metrics.training_samples && (
            <div className="mt-6 pt-6 border-t">
              <h4 className="text-sm font-medium text-gray-600 mb-3">Dataset Information</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="w-4 h-4 text-blue-500" />
                  <span className="text-sm">Training: {metrics.training_samples.toLocaleString()}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Activity className="w-4 h-4 text-green-500" />
                  <span className="text-sm">Testing: {metrics.testing_samples?.toLocaleString()}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Zap className="w-4 h-4 text-purple-500" />
                  <span className="text-sm">Total: {metrics.total_samples?.toLocaleString()}</span>
                </div>
              </div>
            </div>
          )}

          <div className="mt-4 text-xs text-gray-500">
            Last updated: {new Date(metrics.last_updated).toLocaleString()}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

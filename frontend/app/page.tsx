"use client"
import { Header } from "@/components/header"
import { SingleAnalysis } from "@/components/single-analysis"
import { BatchAnalysis } from "@/components/batch-analysis"
import { ModelMetrics } from "@/components/model-metrics"
import { SampleReviews } from "@/components/sample-reviews"
import { Footer } from "@/components/footer"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Healthcare Sentiment Analysis</h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Analyze patient feedback and healthcare reviews using advanced machine learning to understand sentiment
              patterns and improve healthcare services.
            </p>
          </div>

          <Tabs defaultValue="single" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="single">Single Analysis</TabsTrigger>
              <TabsTrigger value="batch">Batch Analysis</TabsTrigger>
              <TabsTrigger value="metrics">Model Performance</TabsTrigger>
              <TabsTrigger value="samples">Sample Reviews</TabsTrigger>
            </TabsList>

            <TabsContent value="single" className="space-y-6">
              <SingleAnalysis />
            </TabsContent>

            <TabsContent value="batch" className="space-y-6">
              <BatchAnalysis />
            </TabsContent>

            <TabsContent value="metrics" className="space-y-6">
              <ModelMetrics />
            </TabsContent>

            <TabsContent value="samples" className="space-y-6">
              <SampleReviews />
            </TabsContent>
          </Tabs>
        </div>
      </main>

      <Footer />
    </div>
  )
}

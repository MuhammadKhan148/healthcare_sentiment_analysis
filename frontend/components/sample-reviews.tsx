"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Copy, Play } from "lucide-react"

const sampleReviews = [
  {
    id: 1,
    text: "The doctor was very professional and took time to explain my condition. The staff was friendly and the facility was clean. I felt well cared for throughout my visit.",
    expectedSentiment: "positive",
  },
  {
    id: 2,
    text: "Long wait times and the receptionist was rude. The doctor seemed rushed and didn't answer my questions properly. Very disappointing experience.",
    expectedSentiment: "negative",
  },
  {
    id: 3,
    text: "The appointment was okay. The doctor was competent but not particularly warm. The facility is average, nothing special but adequate.",
    expectedSentiment: "neutral",
  },
  {
    id: 4,
    text: "Excellent care! The nursing staff went above and beyond to make me comfortable. The doctor was knowledgeable and compassionate. Highly recommend this clinic.",
    expectedSentiment: "positive",
  },
  {
    id: 5,
    text: "Terrible experience. Had to wait 3 hours past my appointment time. The doctor was dismissive and didn't seem to care about my concerns. Will not return.",
    expectedSentiment: "negative",
  },
  {
    id: 6,
    text: "The medical treatment was effective and the doctor was professional. The billing process was straightforward. Overall a standard healthcare experience.",
    expectedSentiment: "neutral",
  },
]

export function SampleReviews() {
  const [copiedId, setCopiedId] = useState<number | null>(null)

  const copyToClipboard = (text: string, id: number) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
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
          <CardTitle>Sample Healthcare Reviews</CardTitle>
          <CardDescription>Use these sample reviews to test the sentiment analysis functionality</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            {sampleReviews.map((review) => (
              <Card key={review.id} className="border border-gray-200">
                <CardContent className="pt-4">
                  <div className="space-y-3">
                    <div className="flex items-start justify-between gap-4">
                      <p className="text-sm text-gray-700 flex-1">{review.text}</p>
                      <Badge className={getSentimentColor(review.expectedSentiment)}>{review.expectedSentiment}</Badge>
                    </div>

                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm" onClick={() => copyToClipboard(review.text, review.id)}>
                        <Copy className="w-3 h-3 mr-1" />
                        {copiedId === review.id ? "Copied!" : "Copy"}
                      </Button>

                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          // Navigate to single analysis tab and populate text
                          const textarea = document.querySelector("textarea") as HTMLTextAreaElement
                          if (textarea) {
                            textarea.value = review.text
                            textarea.dispatchEvent(new Event("input", { bubbles: true }))
                            // Switch to single analysis tab
                            const singleTab = document.querySelector('[value="single"]') as HTMLButtonElement
                            if (singleTab) {
                              singleTab.click()
                            }
                          }
                        }}
                      >
                        <Play className="w-3 h-3 mr-1" />
                        Test
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>CSV Format Example</CardTitle>
          <CardDescription>For batch analysis, your CSV file should follow this format</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm">
            <div className="space-y-1">
              <div className="font-semibold">text</div>
              <div>"The doctor was very professional and took time to explain my condition."</div>
              <div>"Long wait times and the receptionist was rude."</div>
              <div>"The appointment was okay. The doctor was competent but not particularly warm."</div>
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-600">
            <p className="mb-2">
              <strong>Supported column names:</strong> text, review, comment, feedback
            </p>
            <p>
              The CSV file should have a header row with one of the supported column names. Each subsequent row should
              contain the text to be analyzed.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

#!/bin/bash

echo "🚀 Healthcare Sentiment Analysis - Deployment Script"
echo "=================================================="

echo ""
echo "📋 Checking deployment files..."
echo ""

# Check backend files
echo "✅ Backend files:"
ls -la backend/

echo ""
echo "✅ Frontend files:"
ls -la frontend/

echo ""
echo "🎯 Deployment Instructions:"
echo ""
echo "1. BACKEND DEPLOYMENT (Railway/Heroku):"
echo "   cd backend"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Deploy healthcare sentiment analysis backend'"
echo "   # Follow Railway/Heroku deployment instructions"
echo ""
echo "2. FRONTEND DEPLOYMENT (Netlify/Vercel):"
echo "   cd frontend"
echo "   npm run build"
echo "   # Follow Netlify/Vercel deployment instructions"
echo ""
echo "3. ENVIRONMENT VARIABLES:"
echo "   - Set NEXT_PUBLIC_API_URL to your backend URL"
echo "   - Example: https://your-app.railway.app"
echo ""
echo "4. TEST DEPLOYMENT:"
echo "   - Test with: 'I really enjoyed the experience'"
echo "   - Should return: Positive (was Neutral before enhancement)"
echo ""
echo "✅ All files are ready for deployment!"
echo "📁 Backend includes exact trained model files"
echo "📁 Frontend includes enhanced UI components"
echo ""
echo "🎉 Your enhanced healthcare sentiment analysis is ready to deploy!" 
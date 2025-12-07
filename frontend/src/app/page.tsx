'use client'

import { useState } from 'react'
import { UserButton, SignInButton, useUser } from '@clerk/nextjs'
import { SymptomForm } from '@/components/SymptomForm'
import { ResultCard } from '@/components/ResultCard'
import { Activity, Shield, Sparkles, Brain, Clock, Lock, Heart, Zap } from 'lucide-react'

export default function Home() {
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const { isSignedIn, user } = useUser()

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 animate-fade-in">
              <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-xl shadow-lg">
                <Activity className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold gradient-text">
                  HealthAI Assistant
                </h1>
                <p className="text-xs text-gray-500 hidden sm:block">AI-Powered Medical Analysis</p>
              </div>
            </div>
            <div className="flex gap-2 items-center">
              {isSignedIn ? (
                <div className="flex items-center gap-3">
                  <div className="hidden sm:block text-right">
                    <p className="text-sm font-semibold text-gray-900">
                      {user?.firstName || 'User'}
                    </p>
                    <p className="text-xs text-gray-500">Authenticated</p>
                  </div>
                  <UserButton afterSignOutUrl="/" />
                </div>
              ) : (
                <SignInButton mode="modal">
                  <button className="btn-primary text-sm sm:text-base">
                    <Lock className="w-4 h-4 inline mr-2" />
                    Sign In
                  </button>
                </SignInButton>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="text-center mb-12 animate-slide-up">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold mb-6">
            <Sparkles className="w-4 h-4" />
            Powered by Advanced AI & Medical Knowledge Base
          </div>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 mb-6 leading-tight">
            Smart <span className="gradient-text">Symptom Analysis</span><br className="hidden sm:block" />
            at Your Fingertips
          </h2>
          <p className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Get instant, AI-powered health insights with our advanced symptom checker. 
            RAG-enhanced analysis for accurate, reliable results.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12 animate-fade-in">
          <div className="card text-center group hover:scale-105 transition-transform duration-300">
            <div className="bg-gradient-to-br from-blue-100 to-indigo-100 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
              <Brain className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold mb-2 text-gray-900">AI-Powered Analysis</h3>
            <p className="text-gray-600 leading-relaxed">
              Advanced LLM with RAG technology for comprehensive symptom evaluation
            </p>
          </div>
          <div className="card text-center group hover:scale-105 transition-transform duration-300">
            <div className="bg-gradient-to-br from-red-100 to-pink-100 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
              <Shield className="w-8 h-8 text-red-600" />
            </div>
            <h3 className="text-xl font-bold mb-2 text-gray-900">Emergency Detection</h3>
            <p className="text-gray-600 leading-relaxed">
              Real-time safety monitoring with instant emergency alerts
            </p>
          </div>
          <div className="card text-center group hover:scale-105 transition-transform duration-300 sm:col-span-2 lg:col-span-1">
            <div className="bg-gradient-to-br from-green-100 to-emerald-100 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
              <Clock className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-bold mb-2 text-gray-900">Instant Results</h3>
            <p className="text-gray-600 leading-relaxed">
              Get comprehensive analysis in seconds, not hours
            </p>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Symptom Form */}
          <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <SymptomForm onResult={setAnalysisResult} />
          </div>

          {/* Results */}
          <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
            {analysisResult ? (
              <ResultCard result={analysisResult} />
            ) : (
              <div className="card h-full flex items-center justify-center min-h-[400px] bg-gradient-to-br from-gray-50 to-white">
                <div className="text-center text-gray-400">
                  <div className="relative mb-6">
                    <div className="absolute inset-0 bg-blue-100 rounded-full blur-2xl opacity-30 animate-pulse"></div>
                    <Heart className="w-20 h-20 mx-auto opacity-40 relative animate-pulse" />
                  </div>
                  <p className="text-lg font-medium text-gray-500 mb-2">
                    Ready to analyze
                  </p>
                  <p className="text-sm text-gray-400">
                    Fill out the form to get AI-powered insights
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Information Section */}
        <div className="mt-16 card animate-fade-in">
          <h3 className="text-2xl font-bold mb-6 gradient-text flex items-center gap-3">
            <Zap className="w-7 h-7 text-blue-600" />
            How It Works
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold">
                1
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Describe Symptoms</h4>
                <p className="text-gray-600 text-sm">
                  Provide detailed information about what you're experiencing
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold">
                2
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">AI Analysis</h4>
                <p className="text-gray-600 text-sm">
                  Our AI analyzes your symptoms using medical knowledge base
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold">
                3
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Get Insights</h4>
                <p className="text-gray-600 text-sm">
                  Receive comprehensive health insights and recommendations
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 p-6 bg-amber-50 border-2 border-amber-200 rounded-2xl animate-fade-in">
          <div className="flex gap-4">
            <Shield className="w-6 h-6 text-amber-600 flex-shrink-0 mt-1" />
            <div>
              <h4 className="font-bold text-amber-900 mb-2">Medical Disclaimer</h4>
              <p className="text-sm text-amber-800 mb-3">
                This tool provides educational information only and is not a substitute for professional 
                medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional 
                for medical concerns.
              </p>
              <p className="text-sm font-semibold text-amber-900">
                ⚠️ For emergencies, call 112 immediately
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}

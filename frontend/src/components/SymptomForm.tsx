'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Loader2, AlertCircle, Stethoscope, Calendar, User, TrendingUp } from 'lucide-react'
import { toast } from 'sonner'
import { analyzeSymptoms } from '@/lib/api'

interface SymptomFormData {
  symptoms: string
  age?: number
  gender?: string
  medical_history?: string
  duration?: string
  severity?: 'mild' | 'moderate' | 'severe'
}

interface SymptomFormProps {
  onResult: (result: any) => void
}

export function SymptomForm({ onResult }: SymptomFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<SymptomFormData>()

  const onSubmit = async (data: SymptomFormData) => {
    setIsLoading(true)
    
    try {
      // Process medical history
      const medicalHistory = data.medical_history
        ? data.medical_history.split(',').map(item => item.trim())
        : []

      const payload = {
        symptoms: data.symptoms,
        age: data.age,
        gender: data.gender,
        medical_history: medicalHistory.length > 0 ? medicalHistory : undefined,
        duration: data.duration,
        severity: data.severity,
      }

      const result = await analyzeSymptoms(payload)
      
      onResult(result)
      
      if (result.safety_check?.is_emergency) {
        toast.error('Emergency Detected!', {
          description: result.safety_check.warning_message,
        })
      } else {
        toast.success('Analysis Complete', {
          description: 'Your symptom analysis is ready',
        })
      }
    } catch (error: any) {
      toast.error('Analysis Failed', {
        description: error.message || 'Unable to analyze symptoms',
      })
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="card bg-gradient-to-br from-white to-blue-50 border-2 border-blue-100">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2.5 rounded-xl">
          <Stethoscope className="w-6 h-6 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Describe Your Symptoms</h2>
          <p className="text-sm text-gray-500">Provide details for accurate analysis</p>
        </div>
      </div>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        {/* Symptoms */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <Stethoscope className="w-4 h-4 text-blue-600" />
            Symptoms <span className="text-red-500">*</span>
          </label>
          <textarea
            {...register('symptoms', { 
              required: 'Please describe your symptoms',
              minLength: { value: 10, message: 'Please provide more details' }
            })}
            className="input-field min-h-[120px] resize-none"
            placeholder="Describe your symptoms in detail... (e.g., headache, fever, cough)"
            disabled={isLoading}
          />
          {errors.symptoms && (
            <p className="text-red-500 text-sm font-medium flex items-center gap-1.5 animate-slide-up">
              <AlertCircle className="w-4 h-4" />
              {errors.symptoms.message}
            </p>
          )}
        </div>

        {/* Age and Gender */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <User className="w-4 h-4 text-blue-600" />
              Age
            </label>
            <input
              type="number"
              {...register('age', { 
                min: { value: 0, message: 'Invalid age' },
                max: { value: 120, message: 'Invalid age' }
              })}
              className="input-field"
              placeholder="Your age"
              disabled={isLoading}
            />
            {errors.age && (
              <p className="text-red-500 text-xs font-medium animate-slide-up">{errors.age.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <User className="w-4 h-4 text-blue-600" />
              Gender
            </label>
            <select
              {...register('gender')}
              className="input-field"
              disabled={isLoading}
            >
              <option value="">Select...</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="prefer_not_to_say">Prefer not to say</option>
            </select>
          </div>
        </div>

        {/* Duration and Severity */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <Calendar className="w-4 h-4 text-blue-600" />
              Duration
            </label>
            <input
              type="text"
              {...register('duration')}
              className="input-field"
              placeholder="e.g., 3 days, 2 weeks"
              disabled={isLoading}
            />
          </div>

          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
              <TrendingUp className="w-4 h-4 text-blue-600" />
              Severity
            </label>
            <select
              {...register('severity')}
              className="input-field"
              disabled={isLoading}
            >
              <option value="">Select...</option>
              <option value="mild">😊 Mild</option>
              <option value="moderate">😐 Moderate</option>
              <option value="severe">😣 Severe</option>
            </select>
          </div>
        </div>

        {/* Medical History */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <AlertCircle className="w-4 h-4 text-blue-600" />
            Medical History
          </label>
          <input
            type="text"
            {...register('medical_history')}
            className="input-field"
            placeholder="Existing conditions (comma-separated)"
            disabled={isLoading}
          />
          <p className="text-xs text-gray-500 flex items-center gap-1">
            <span className="text-blue-600">💡</span>
            e.g., diabetes, hypertension, asthma
          </p>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary w-full flex items-center justify-center gap-2 text-base font-semibold py-3.5 shadow-lg hover:shadow-xl"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing with AI...
            </>
          ) : (
            <>
              <Stethoscope className="w-5 h-5" />
              Analyze Symptoms
            </>
          )}
        </button>

        {/* Reset Button */}
        {!isLoading && (
          <button
            type="button"
            onClick={() => reset()}
            className="btn-secondary w-full font-medium"
          >
            Clear Form
          </button>
        )}
      </form>

      {/* Warning Notice */}
      <div className="mt-6 p-4 bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-xl">
        <p className="text-sm text-amber-900 font-medium leading-relaxed">
          <strong className="flex items-center gap-2 mb-1">
            ⚠️ Important Notice
          </strong>
          This is an AI-powered symptom analysis tool for educational purposes.
          For medical emergencies, <span className="font-bold text-red-600">call 112 immediately</span>.
        </p>
      </div>
    </div>
  )
}

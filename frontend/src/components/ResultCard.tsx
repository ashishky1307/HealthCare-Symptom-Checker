'use client'

import { 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  AlertCircle,
  Brain,
  Pill,
  Building2,
  Phone,
  ClipboardList,
  TrendingUp,
  Clock,
  Shield,
  Heart
} from 'lucide-react'

interface ResultCardProps {
  result: any
}

export function ResultCard({ result }: ResultCardProps) {
  const { status, safety_check, analysis, recommendations, disclaimer } = result

  // Determine severity color
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-gradient-to-r from-red-50 to-red-100 border-red-500'
      case 'urgent':
        return 'bg-gradient-to-r from-orange-50 to-orange-100 border-orange-500'
      case 'moderate':
        return 'bg-gradient-to-r from-yellow-50 to-yellow-100 border-yellow-500'
      default:
        return 'bg-gradient-to-r from-green-50 to-green-100 border-green-500'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
      case 'urgent':
        return <AlertTriangle className="w-7 h-7 text-red-600" />
      case 'moderate':
        return <Info className="w-7 h-7 text-yellow-600" />
      default:
        return <CheckCircle className="w-7 h-7 text-green-600" />
    }
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Safety Check Card */}
      {safety_check && (
        <div className={`card border-l-4 ${getSeverityColor(safety_check.severity)} animate-slide-up`}>
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 p-3 bg-white rounded-xl shadow-md">
              {getSeverityIcon(safety_check.severity)}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                {safety_check.is_emergency && (
                  <span className="badge bg-red-600 text-white text-xs animate-pulse">
                    EMERGENCY
                  </span>
                )}
                <h3 className="text-2xl font-bold text-gray-900">
                  {safety_check.is_emergency ? '🚨 Emergency Detected' : 'Safety Assessment'}
                </h3>
              </div>
              <p className="text-lg font-semibold text-gray-800 mb-3">
                {safety_check.recommendation}
              </p>
              
              {safety_check.warning_message && (
                <div className="mt-4 p-4 bg-white border-2 border-current rounded-xl shadow-sm">
                  <div className="flex items-center gap-2 mb-2">
                    <Shield className="w-5 h-5" />
                    <h4 className="font-bold">Warning Message:</h4>
                  </div>
                  <p className="font-semibold text-gray-900">{safety_check.warning_message}</p>
                  {safety_check.is_emergency && (
                    <div className="mt-3 p-3 bg-red-100 rounded-lg border-2 border-red-300">
                      <p className="text-red-900 font-bold flex items-center gap-2">
                        <Phone className="w-5 h-5" />
                        Call 112 immediately for emergency assistance
                      </p>
                    </div>
                  )}
                </div>
              )}

              {safety_check.matched_keywords?.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-semibold text-gray-700 mb-2">
                    Detected Keywords:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {safety_check.matched_keywords.map((keyword: string, idx: number) => (
                      <span
                        key={idx}
                        className="badge bg-white border-2 border-current text-sm font-medium"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {analysis && status !== 'emergency' && (
        <div className="card bg-gradient-to-br from-white to-blue-50 animate-slide-up border-2 border-blue-100">
          <div className="flex items-center gap-3 mb-6">
            <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2.5 rounded-xl">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900">AI Analysis Results</h3>
          </div>

          {/* Possible Conditions */}
          {analysis.possible_conditions && (
            <div className="mb-6 p-5 bg-white rounded-xl border-2 border-blue-100 shadow-sm">
              <h4 className="font-bold text-lg mb-4 flex items-center gap-2 text-gray-900">
                <ClipboardList className="w-5 h-5 text-blue-600" />
                Possible Conditions:
              </h4>
              <ul className="space-y-3">
                {analysis.possible_conditions.map((condition: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3 group">
                    <div className="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mt-0.5 group-hover:bg-blue-200 transition-colors">
                      <span className="text-blue-700 font-bold text-sm">{idx + 1}</span>
                    </div>
                    <span className="text-gray-800 leading-relaxed">{condition}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Severity Assessment */}
          {analysis.severity_assessment && (
            <div className="mb-6 p-5 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border-2 border-indigo-200">
              <h4 className="font-bold text-lg mb-3 flex items-center gap-2 text-gray-900">
                <TrendingUp className="w-5 h-5 text-indigo-600" />
                Severity Assessment:
              </h4>
              <p className="text-gray-800 leading-relaxed">{analysis.severity_assessment}</p>
            </div>
          )}

          {/* Recommended Actions */}
          {analysis.recommended_actions && (
            <div className="mb-6 p-5 bg-white rounded-xl border-2 border-green-100 shadow-sm">
              <h4 className="font-bold text-lg mb-4 flex items-center gap-2 text-gray-900">
                <Building2 className="w-5 h-5 text-green-600" />
                Recommended Actions:
              </h4>
              <ol className="space-y-3">
                {analysis.recommended_actions.map((action: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mt-0.5">
                      <span className="text-green-700 font-bold text-sm">{idx + 1}</span>
                    </div>
                    <span className="text-gray-800 leading-relaxed">{action}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* Self-Care Tips */}
          {analysis.self_care_tips && (
            <div className="mb-6 p-5 bg-white rounded-xl border-2 border-emerald-100 shadow-sm">
              <h4 className="font-bold text-lg mb-4 flex items-center gap-2 text-gray-900">
                <Heart className="w-5 h-5 text-emerald-600" />
                Self-Care Tips:
              </h4>
              <ul className="space-y-3">
                {analysis.self_care_tips.map((tip: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3 group">
                    <CheckCircle className="w-5 h-5 text-emerald-600 mt-0.5 flex-shrink-0 group-hover:scale-110 transition-transform" />
                    <span className="text-gray-800 leading-relaxed">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Red Flags */}
          {analysis.red_flags && (
            <div className="mb-6 p-5 bg-gradient-to-br from-red-50 to-pink-50 border-2 border-red-300 rounded-xl">
              <h4 className="font-bold text-lg mb-4 text-red-900 flex items-center gap-2">
                <AlertCircle className="w-6 h-6" />
                Warning Signs to Watch For:
              </h4>
              <ul className="space-y-3">
                {analysis.red_flags.map((flag: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3">
                    <span className="text-xl flex-shrink-0 mt-0.5">⚠️</span>
                    <span className="text-red-900 font-medium leading-relaxed">{flag}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* When to Seek Care */}
          {analysis.when_to_seek_care && (
            <div className="p-5 bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-300 rounded-xl">
              <h4 className="font-bold text-lg mb-3 flex items-center gap-2 text-amber-900">
                <Clock className="w-5 h-5" />
                When to Seek Medical Care:
              </h4>
              <p className="text-amber-900 font-medium leading-relaxed">{analysis.when_to_seek_care}</p>
            </div>
          )}

          {/* Confidence Level */}
          {analysis.confidence_level && (
            <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-blue-100 rounded-full">
              <Brain className="w-4 h-4 text-blue-700" />
              <p className="text-sm font-semibold text-blue-900">
                Confidence: {analysis.confidence_level}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Recommendations Summary */}
      {recommendations && recommendations.length > 0 && (
        <div className="card bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 animate-slide-up">
          <div className="flex items-center gap-3 mb-5">
            <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2.5 rounded-xl">
              <Pill className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900">Key Recommendations</h3>
          </div>
          <ul className="space-y-3">
            {recommendations.map((rec: string, idx: number) => (
              <li key={idx} className="flex items-start gap-3 p-3 bg-white rounded-lg hover:shadow-md transition-shadow">
                <span className="text-blue-600 font-bold mt-1 flex-shrink-0">→</span>
                <span className="text-gray-800 leading-relaxed">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

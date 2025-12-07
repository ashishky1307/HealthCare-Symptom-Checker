"""Direct symptom analysis using Groq LLM with RAG enhancement."""

from groq import Groq
import json
import logging
from typing import Dict, List, Optional, Any
import os
from services.rag_service import get_rag_service

logger = logging.getLogger(__name__)


class SymptomAnalyzer:
    """Analyze symptoms directly using Groq LLM with RAG enhancement."""
    
    def __init__(self):
        """Initialize Groq client and RAG service."""
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=groq_api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        # Initialize RAG service
        try:
            self.rag_service = get_rag_service()
            self.rag_enabled = True
            logger.info("✅ RAG service initialized successfully")
        except Exception as e:
            logger.warning(f"RAG service initialization failed: {e}. Continuing without RAG.")
            self.rag_service = None
            self.rag_enabled = False
        
        logger.info(f"✅ SymptomAnalyzer initialized with Groq ({self.model}) and RAG: {self.rag_enabled}")
    
    async def analyze(
        self,
        symptoms: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        medical_history: Optional[List[str]] = None,
        duration: Optional[str] = None,
        severity: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze symptoms using Groq LLM.
        
        Returns structured analysis with:
        - Emergency assessment
        - Possible conditions
        - Recommendations
        - When to seek care
        """
        try:
            # Check for emergency keywords first
            emergency_check = self._check_emergency(symptoms)
            
            # Build context
            context = self._build_context(
                symptoms, age, gender, medical_history, duration, severity
            )
            
            # Retrieve relevant medical knowledge using RAG
            rag_context = ""
            if self.rag_enabled and self.rag_service:
                try:
                    relevant_chunks = self.rag_service.retrieve_relevant_context(
                        query=symptoms,
                        n_results=5,
                        min_relevance_score=0.3
                    )
                    if relevant_chunks:
                        rag_context = self.rag_service.format_context_for_llm(
                            relevant_chunks,
                            max_chunks=3
                        )
                        logger.info(f"✓ Retrieved {len(relevant_chunks)} relevant knowledge chunks")
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {e}. Continuing without RAG context.")
            
            # Create prompt with RAG context
            prompt = self._create_prompt(context, emergency_check, rag_context)
            
            # Call Groq
            logger.info(f"Analyzing symptoms with Groq: {symptoms[:50]}...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a medical AI assistant for symptom analysis. "
                            "Provide structured, helpful analysis while being clear that "
                            "this is NOT a diagnosis and professional medical consultation is needed. "
                            "Format response as JSON with these fields: "
                            "possible_conditions, severity_assessment, recommended_actions, "
                            "self_care_tips, red_flags, when_to_seek_emergency_care"
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            analysis = json.loads(response.choices[0].message.content)
            
            # Transform LLM response to match schema requirements
            transformed_analysis = self._transform_analysis(analysis)
            
            # Structure final response to match SymptomAnalysisResponse schema
            result = {
                "status": "emergency" if emergency_check["is_emergency"] else "success",
                "safety_check": {
                    "is_emergency": emergency_check["is_emergency"],
                    "severity": emergency_check["severity"],
                    "matched_keywords": emergency_check["keywords"],
                    "recommendation": self._get_safety_recommendation(emergency_check),
                    "should_call_112": emergency_check["is_emergency"],
                    "should_seek_immediate_care": emergency_check["severity"] == "urgent"
                },
                "analysis": transformed_analysis,
                "recommendations": transformed_analysis.get("recommended_actions", []),
                "disclaimer": (
                    "⚠️ EDUCATIONAL INFORMATION ONLY - NOT MEDICAL ADVICE ⚠️\n\n"
                    "This AI-powered analysis is provided for educational and informational purposes only. "
                    "It is NOT intended to be a substitute for professional medical advice, diagnosis, or treatment. "
                    "The information provided should not be used for diagnosing or treating a health problem or disease. \n\n"
                    "IMPORTANT: Always seek the advice of your physician or other qualified health provider "
                    "with any questions you may have regarding a medical condition. Never disregard professional "
                    "medical advice or delay seeking it because of information from this system. \n\n"
                    "This system uses artificial intelligence which may make errors or provide incomplete information. "
                    "All suggestions must be verified with a qualified healthcare professional before taking any action."
                )
            }
            
            logger.info(f"✓ Analysis complete. Emergency: {result['safety_check']['is_emergency']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in symptom analysis: {e}")
            # Return fallback response
            return self._fallback_response(symptoms, emergency_check)
    
    def _check_emergency(self, symptoms: str) -> Dict[str, Any]:
        """Check for emergency keywords."""
        symptoms_lower = symptoms.lower()
        
        # Critical emergency keywords
        critical_keywords = [
            "chest pain", "heart attack", "can't breathe", "difficulty breathing",
            "severe bleeding", "unconscious", "seizure", "stroke",
            "suicide", "severe burns", "poisoning", "choking"
        ]
        
        # Urgent keywords
        urgent_keywords = [
            "high fever", "severe pain", "blood in", "confusion",
            "severe headache", "stiff neck", "sudden weakness"
        ]
        
        found_critical = [kw for kw in critical_keywords if kw in symptoms_lower]
        found_urgent = [kw for kw in urgent_keywords if kw in symptoms_lower]
        
        if found_critical:
            return {
                "is_emergency": True,
                "severity": "critical",
                "keywords": found_critical
            }
        elif found_urgent:
            return {
                "is_emergency": False,
                "severity": "urgent",
                "keywords": found_urgent
            }
        else:
            return {
                "is_emergency": False,
                "severity": "moderate",
                "keywords": []
            }
    
    def _build_context(
        self,
        symptoms: str,
        age: Optional[int],
        gender: Optional[str],
        medical_history: Optional[List[str]],
        duration: Optional[str],
        severity: Optional[str]
    ) -> str:
        """Build patient context string."""
        context_parts = [f"Symptoms: {symptoms}"]
        
        if age:
            context_parts.append(f"Age: {age}")
        if gender:
            context_parts.append(f"Gender: {gender}")
        if medical_history:
            context_parts.append(f"Medical History: {', '.join(medical_history)}")
        if duration:
            context_parts.append(f"Duration: {duration}")
        if severity:
            context_parts.append(f"Severity: {severity}")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, context: str, emergency_check: Dict[str, Any], rag_context: str = "") -> str:
        """Create analysis prompt for LLM with optional RAG context."""
        if emergency_check["is_emergency"]:
            emergency_note = (
                f"\n⚠️ EMERGENCY DETECTED: {', '.join(emergency_check['keywords'])}\n"
                "Prioritize immediate emergency care recommendations."
            )
        else:
            emergency_note = ""
        
        # Add RAG context if available
        knowledge_section = ""
        if rag_context:
            knowledge_section = f"\n\n{rag_context}\n\nUse the above medical knowledge to inform your analysis, but adapt it to the specific patient context.\n"
        
        prompt = f"""Analyze the following patient presentation:

{context}{emergency_note}{knowledge_section}

Provide a comprehensive analysis in JSON format with:

1. possible_conditions: Array of potential diagnoses with reasoning
2. severity_assessment: Overall severity level and explanation
3. recommended_actions: Step-by-step actions the patient should take
4. self_care_tips: Safe home care recommendations
5. red_flags: Warning signs that require immediate attention
6. when_to_seek_emergency_care: Specific circumstances requiring 112/ER

Be thorough but emphasize the importance of professional medical evaluation.
"""
        return prompt
    
    def _transform_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Transform LLM analysis response to match schema."""
        # Transform possible_conditions (can be array of objects or strings)
        conditions = analysis.get("possible_conditions", [])
        if isinstance(conditions, str):
            # If it's a string, wrap it in a list
            conditions = [conditions] if conditions else []
        elif conditions and isinstance(conditions, list) and len(conditions) > 0 and isinstance(conditions[0], dict):
            # Convert objects to strings
            conditions = [
                f"{c.get('condition', c.get('name', 'Unknown'))}: {c.get('reasoning', '')}"
                for c in conditions
            ]
        elif not isinstance(conditions, list):
            conditions = []
        
        # Transform severity_assessment (can be object or string)
        severity = analysis.get("severity_assessment", "")
        if isinstance(severity, dict):
            severity = f"{severity.get('level', 'Unknown')} - {severity.get('explanation', severity.get('reasoning', ''))}"
        elif not isinstance(severity, str):
            severity = str(severity)
        
        # Transform recommended_actions (extract strings from objects or convert string to list)
        recommended_actions = analysis.get("recommended_actions", [])
        if isinstance(recommended_actions, str):
            # If it's a string, wrap it in a list
            recommended_actions = [recommended_actions] if recommended_actions else []
        elif recommended_actions and isinstance(recommended_actions, list) and len(recommended_actions) > 0 and isinstance(recommended_actions[0], dict):
            recommended_actions = [
                action.get('action', action.get('step', str(action)))
                for action in recommended_actions
            ]
        elif not isinstance(recommended_actions, list):
            recommended_actions = []
        
        # Transform self_care_tips (extract strings from objects or convert string to list)
        self_care_tips = analysis.get("self_care_tips", [])
        if isinstance(self_care_tips, str):
            # If it's a string, wrap it in a list
            self_care_tips = [self_care_tips] if self_care_tips else []
        elif self_care_tips and isinstance(self_care_tips, list) and len(self_care_tips) > 0 and isinstance(self_care_tips[0], dict):
            self_care_tips = [
                tip.get('tip', tip.get('recommendation', str(tip)))
                for tip in self_care_tips
            ]
        elif not isinstance(self_care_tips, list):
            self_care_tips = []
        
        # Transform red_flags (extract strings from objects or convert string to list)
        red_flags = analysis.get("red_flags", [])
        if isinstance(red_flags, str):
            # If it's a string, wrap it in a list
            red_flags = [red_flags] if red_flags else []
        elif red_flags and isinstance(red_flags, list) and len(red_flags) > 0 and isinstance(red_flags[0], dict):
            red_flags = [
                flag.get('flag', flag.get('warning', str(flag)))
                for flag in red_flags
            ]
        elif not isinstance(red_flags, list):
            red_flags = []
        
        # Transform when_to_seek_care (can be object or string)
        when_to_seek = analysis.get("when_to_seek_emergency_care", "")
        if isinstance(when_to_seek, dict):
            circumstances = when_to_seek.get("circumstances", [])
            instruction = when_to_seek.get("instruction", "")
            when_to_seek = f"{instruction} Circumstances: {', '.join(circumstances)}"
        elif isinstance(when_to_seek, list):
            when_to_seek = " ".join(when_to_seek)
        
        return {
            "possible_conditions": conditions,
            "severity_assessment": severity,
            "recommended_actions": recommended_actions,
            "when_to_seek_care": when_to_seek,
            "self_care_tips": self_care_tips,
            "red_flags": red_flags,
            "confidence_level": "moderate"
        }
    
    def _get_safety_recommendation(self, emergency_check: Dict[str, Any]) -> str:
        """Get safety recommendation based on emergency check."""
        if emergency_check["is_emergency"]:
            return (
                "🚨 EMERGENCY: Based on your symptoms, this may require IMMEDIATE medical attention. "
                "Call 112 or go to the nearest emergency room NOW. Do not wait or rely on this analysis alone."
            )
        elif emergency_check["severity"] == "urgent":
            return (
                "⚠️ URGENT: Your symptoms suggest you should seek medical attention soon. "
                "Contact your healthcare provider or visit an urgent care facility within 24 hours. "
                "This is educational information - professional medical evaluation is essential."
            )
        else:
            return (
                "This analysis is for educational purposes. Monitor your symptoms and consult "
                "a healthcare provider if they persist, worsen, or if you have concerns. "
                "Professional medical advice is always recommended for accurate diagnosis."
            )
    
    def _fallback_response(
        self,
        symptoms: str,
        emergency_check: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Return basic fallback response if LLM fails."""
        recommendation = self._get_safety_recommendation(emergency_check)
        
        return {
            "status": "emergency" if emergency_check["is_emergency"] else "fallback",
            "safety_check": {
                "is_emergency": emergency_check["is_emergency"],
                "severity": emergency_check["severity"],
                "matched_keywords": emergency_check["keywords"],
                "recommendation": recommendation,
                "should_call_112": emergency_check["is_emergency"],
                "should_seek_immediate_care": emergency_check["severity"] == "urgent"
            },
            "analysis": {
                "possible_conditions": ["Unable to determine (analysis service unavailable)"],
                "severity_assessment": f"{emergency_check['severity']} - Based on symptoms: {symptoms}",
                "recommended_actions": [recommendation],
                "when_to_seek_care": "If symptoms worsen, persist, or you feel this is a medical emergency, seek immediate medical care.",
                "self_care_tips": ["Rest", "Stay hydrated", "Monitor symptoms"],
                "red_flags": ["Worsening symptoms", "High fever", "Difficulty breathing"],
                "confidence_level": "low"
            },
            "recommendations": [recommendation],
            "disclaimer": (
                "⚠️ EDUCATIONAL INFORMATION ONLY - NOT MEDICAL ADVICE ⚠️\n\n"
                "This AI-powered analysis is provided for educational and informational purposes only. "
                "It is NOT intended to be a substitute for professional medical advice, diagnosis, or treatment. "
                "Always seek the advice of your physician or other qualified health provider."
            )
        }

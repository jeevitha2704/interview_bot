import os
import json
import random
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # OpenAI may not be available in some environments


class QuestionGenerator:
    """Generate interview questions based on resume data.

    This class will attempt to use the OpenAI client when an API key is
    provided and available. If OpenAI is unavailable or the API call fails
    (for example insufficient quota), it will fall back to generating
    rule-based questions locally so the UI remains testable.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key (optional)."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.use_openai = False
        self.model = "gpt-3.5-turbo"

        if self.api_key and OpenAI is not None:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.use_openai = True
            except Exception:
                # If client creation fails, fall back to local generator
                self.client = None
                self.use_openai = False
    
    def generate_questions(self, resume_data, num_questions=5, question_type='mixed'):
        """
        Generate interview questions based on resume data
        
        Args:
            resume_data: Dict with parsed resume information
            num_questions: Number of questions to generate
            question_type: 'technical', 'behavioral', 'mixed'
        
        Returns:
            List of generated interview questions
        """
        # If OpenAI is available and configured, try using it first.
        if self.use_openai and self.client is not None:
            try:
                prompt = self._build_prompt(resume_data, num_questions, question_type)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert technical interviewer. Generate thoughtful, relevant interview questions based on the candidate's resume. Each question should be specific to their experience and skills."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )

                questions_text = response.choices[0].message.content
                questions = self._parse_questions(questions_text)

                return {
                    'questions': questions,
                    'count': len(questions),
                    'type': question_type
                }

            except Exception:
                # Fall through to local fallback when OpenAI fails (quota, network, etc.)
                self.use_openai = False

        # Local fallback generator (rule-based)
        questions = self._local_fallback_questions(resume_data, num_questions, question_type)
        return {
            'questions': questions,
            'count': len(questions),
            'type': question_type,
            'fallback': True
        }
    
    def _build_prompt(self, resume_data, num_questions, question_type):
        """Build the prompt for GPT"""
        skills = ', '.join(resume_data.get('skills', [])[:8])
        experience = '\n'.join(resume_data.get('experience', [])[:3])
        education = ', '.join(resume_data.get('education', []))
        
        prompt = f"""
Based on the following resume information, generate {num_questions} {question_type} interview questions:

SKILLS: {skills}

EXPERIENCE:
{experience}

EDUCATION: {education}

KEY HIGHLIGHTS:
{chr(10).join(resume_data.get('key_highlights', [])[:3])}

Generate {num_questions} interview questions that:
1. Are specific to the candidate's experience and skills
2. Are designed to assess their expertise and problem-solving abilities
3. Range from technical depth to behavioral insights

Format each question on a new line starting with the question number (e.g., "1. ")
"""
        return prompt
    
    def _parse_questions(self, response_text):
        """Parse questions from GPT response"""
        lines = response_text.strip().split('\n')
        questions = []
        
        for line in lines:
            # Clean and extract question text
            line = line.strip()
            if not line:
                continue
            
            # Remove numbering if present
            if line[0].isdigit() and '.' in line[:3]:
                line = line.split('.', 1)[1].strip()
            
            if line:
                questions.append(line)
        
        return questions

    def _local_fallback_questions(self, resume_data: Dict[str, Any], num_questions: int, question_type: str) -> List[str]:
        """Generate simple rule-based questions from parsed resume data.

        This is used as a fallback when OpenAI is not available or fails.
        """
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', [])
        highlights = resume_data.get('key_highlights', [])

        questions: List[str] = []

        # Prefer questions tied to concrete skills/experience
        idx = 0
        while len(questions) < num_questions:
            if question_type in ('technical', 'mixed') and idx < len(skills):
                skill = skills[idx]
                questions.append(f"Explain a project where you used {skill}. What technical challenges did you face and how did you solve them?")
            elif question_type in ('behavioral', 'mixed') and idx < len(experience):
                exp = experience[idx]
                questions.append(f"Tell me about your role at {exp}. What was a significant challenge and how did you handle it?")
            elif idx < len(highlights):
                q = highlights[idx]
                questions.append(f"You mentioned: '{q}'. Can you describe the impact and metrics for this accomplishment?")
            else:
                # Generic fallback question
                if question_type == 'technical':
                    questions.append("Describe an architecture you designed and why you made those technology choices.")
                elif question_type == 'behavioral':
                    questions.append("Describe a time you had to work with a difficult stakeholder and how you managed the situation.")
                else:
                    questions.append("Walk me through a challenging project you worked on and the outcome.")

            idx += 1

        return questions[:num_questions]
    
    def generate_followup_question(self, previous_question, candidate_answer, resume_data):
        """Generate a follow-up question based on candidate's response"""
        # Try OpenAI if available
        if self.use_openai and self.client is not None:
            try:
                prompt = f"""
Previous interview question: "{previous_question}"

Candidate's answer: "{candidate_answer}"

Resume context:
- Skills: {', '.join(resume_data.get('skills', [])[:5])}
- Experience: {resume_data.get('experience', ['N/A'])[0]}

Generate a thoughtful follow-up question that:
1. Digs deeper into the candidate's response
2. Tests their knowledge further
3. Is specific to their answer and background

Just provide the question, nothing else.
"""
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert technical interviewer generating follow-up questions."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=200
                )

                return response.choices[0].message.content.strip()
            except Exception:
                self.use_openai = False

        # Local fallback follow-up
        return f"Can you expand on '{candidate_answer.split('.')[0]}' and explain the key decisions you made?"
    
    def evaluate_answer(self, question, answer, resume_data):
        """Evaluate candidate's answer"""
        skills = resume_data.get('skills', [])

        # Try OpenAI evaluation first
        if self.use_openai and self.client is not None:
            try:
                prompt = f"""
Interview Question: "{question}"

Candidate's Answer: "{answer}"

Candidate's Background:
- Skills: {', '.join(skills[:5])}
- Experience: {resume_data.get('experience', ['N/A'])[0]}

Provide a brief evaluation (2-3 sentences) of the candidate's answer on:
1. Relevance to their background
2. Depth of knowledge shown
3. Overall quality of response

Format: Provide a score (1-10) and brief feedback.
"""
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at evaluating interview answers."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=300
                )

                return response.choices[0].message.content.strip()
            except Exception:
                self.use_openai = False

        # Local simple evaluation fallback
        score = 6
        if any(k.lower() in answer.lower() for k in skills[:3]):
            score += 2
        feedback = f"Score: {score}/10. The answer addresses relevant skills and shows understanding; consider adding more concrete metrics and implementation details."
        return feedback

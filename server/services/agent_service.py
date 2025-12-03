import sys
import os
from pathlib import Path

# Add the agent directory to the path
agent_dir = Path(__file__).parent.parent.parent / "agent"
# Insert at position 0 to ensure agent's modules are found first
if str(agent_dir) not in sys.path:
    sys.path.insert(0, str(agent_dir))

# Import agent modules - these will use the agent's config.py
from lesson_agent import LanguageLearningAgent, LessonPlan


class AgentService:
    """Service to interact with the Language Learning Agent"""

    def __init__(self):
        self.agent = None

    def _get_agent(self) -> LanguageLearningAgent:
        """Lazy load the agent"""
        if self.agent is None:
            self.agent = LanguageLearningAgent()
        return self.agent

    async def generate_lesson_plan(self, transcript: str) -> dict:
        """
        Generate a lesson plan from a transcript.

        Args:
            transcript: The transcribed text from the video

        Returns:
            Dictionary containing the lesson plan
        """
        try:
            agent = self._get_agent()
            lesson_plan: LessonPlan = agent.generate_lesson_plan(transcript)

            # Convert to dictionary for JSON response
            return {
                "detected_language": lesson_plan.detected_language,
                "proficiency_level": lesson_plan.proficiency_level,
                "summary": lesson_plan.summary,
                "vocabulary_words": [
                    {
                        "word": word.word,
                        "translation": word.translation,
                        "definition": word.definition,
                        "example_sentence": word.example_sentence
                    }
                    for word in lesson_plan.vocabulary_words
                ],
                "sentence_structures": [
                    {
                        "structure_name": structure.structure_name,
                        "explanation": structure.explanation,
                        "example_from_text": structure.example_from_text,
                        "practice_template": structure.practice_template
                    }
                    for structure in lesson_plan.sentence_structures
                ],
                "learning_objectives": lesson_plan.learning_objectives,
                "comprehension_questions": [
                    {
                        "question": q.question,
                        "question_type": q.question_type,
                        "correct_answer": q.correct_answer,
                        "options": q.options,
                        "explanation": q.explanation
                    }
                    for q in lesson_plan.comprehension_questions
                ]
            }
        except Exception as e:
            raise Exception(f"Error generating lesson plan: {str(e)}")


# Global instance
agent_service = AgentService()

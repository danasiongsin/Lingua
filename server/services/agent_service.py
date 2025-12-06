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

    async def generate_detailed_info(self, item_type: str, word: str, translation: str = None,
                                     structure_name: str = None) -> dict:
        """
        Generate detailed information and additional examples for vocabulary or grammar.

        Args:
            item_type: Either 'vocab' or 'grammar'
            word: The vocabulary word (for vocab) or structure name (for grammar)
            translation: Translation of the word (for vocab only)
            structure_name: Name of the grammar structure (for grammar only)

        Returns:
            Dictionary containing detailed description and examples
        """
        try:
            agent = self._get_agent()

            if item_type == 'vocab':
                prompt = f"""Provide a detailed linguistic analysis of the word "{word}" ({translation}).

Include:
1. A deeper description covering:
   - Etymology and word origin
   - Nuanced meanings and connotations
   - Register (formal/informal) and usage contexts
   - Common collocations (words it's frequently used with)
   - Any idiomatic expressions using this word

2. Five diverse example sentences demonstrating:
   - Different contexts (casual, formal, professional, etc.)
   - Different grammatical constructions
   - Different meanings if the word is polysemous

Format your response as:
DESCRIPTION:
[Your detailed description here]

EXAMPLES:
1. [Example sentence 1]
2. [Example sentence 2]
3. [Example sentence 3]
4. [Example sentence 4]
5. [Example sentence 5]"""

            else:  # grammar
                prompt = f"""Provide a comprehensive explanation of the grammar structure "{structure_name}".

Include:
1. A deeper description covering:
   - Detailed grammatical explanation
   - When and why this structure is used
   - Common mistakes learners make
   - Comparison with similar structures
   - Register and formality level

2. Five diverse example sentences showing:
   - Different contexts and situations
   - Variations of the structure
   - Common vs. advanced usage
   - Contrasts with alternative structures

Format your response as:
DESCRIPTION:
[Your detailed description here]

EXAMPLES:
1. [Example sentence 1]
2. [Example sentence 2]
3. [Example sentence 3]
4. [Example sentence 4]
5. [Example sentence 5]"""

            # Use the agent's LLM to generate the response
            from langchain_core.messages import HumanMessage

            response = agent.llm.invoke([HumanMessage(content=prompt)])
            content = response.content

            # Parse the response
            parts = content.split("EXAMPLES:")
            description = parts[0].replace("DESCRIPTION:", "").strip()

            examples = []
            if len(parts) > 1:
                example_lines = parts[1].strip().split("\n")
                for line in example_lines:
                    line = line.strip()
                    # Remove numbering (1. 2. etc.) from examples
                    if line and len(line) > 2:
                        # Remove leading numbers and dots
                        cleaned = line.lstrip("0123456789. ").strip()
                        if cleaned:
                            examples.append(cleaned)

            return {
                "description": description,
                "examples": examples[:5]  # Ensure we only return 5 examples
            }

        except Exception as e:
            raise Exception(f"Error generating detailed info: {str(e)}")


# Global instance
agent_service = AgentService()

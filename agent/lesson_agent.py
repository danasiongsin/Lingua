from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from config import config
import re
import json


class VocabularyWord(BaseModel):
    """A vocabulary word to focus on in the lesson"""
    word: str = Field(description="The vocabulary word in the target language")
    translation: str = Field(description="Translation to English")
    definition: str = Field(description="Definition or explanation in context")
    example_sentence: str = Field(description="Example sentence using this word from the monologue or similar")


class SentenceStructure(BaseModel):
    """A grammatical structure to focus on in the lesson"""
    structure_name: str = Field(description="Name of the grammatical structure (e.g., 'Past Tense', 'Conditional')")
    explanation: str = Field(description="Brief explanation of the structure")
    example_from_text: str = Field(description="Example sentence from the monologue demonstrating this structure")
    practice_template: str = Field(description="A template or pattern for students to practice")


class ComprehensionQuestion(BaseModel):
    """A comprehension check question about the monologue"""
    question: str = Field(description="The question text in English")
    question_type: str = Field(description="Type of question: 'multiple_choice', 'true_false', or 'fill_blank'")
    correct_answer: str = Field(description="The correct answer")
    options: List[str] = Field(description="For multiple choice: list of 4 options including the correct one. For true/false: ['True', 'False']. For fill-in-blank: empty list []")
    explanation: str = Field(description="Brief explanation of why this is the correct answer")


class LessonPlan(BaseModel):
    """Complete lesson plan generated from a monologue"""
    detected_language: str = Field(description="The language of the monologue")
    proficiency_level: str = Field(description="Estimated proficiency level (A1, A2, B1, B2, C1, C2)")
    summary: str = Field(description="Brief summary of the monologue content")
    vocabulary_words: List[VocabularyWord] = Field(description="Key vocabulary words to teach")
    sentence_structures: List[SentenceStructure] = Field(description="Important sentence structures to focus on")
    learning_objectives: List[str] = Field(description="Learning objectives for this lesson")
    comprehension_questions: List[ComprehensionQuestion] = Field(description="5-8 comprehension check questions to assess understanding")


class LanguageLearningAgent:
    """LangChain agent using Google Gemini to generate lesson plans from foreign language monologues"""

    def __init__(self):
        """Initialize the agent with Gemini model"""
        config.validate()

        self.llm = ChatGoogleGenerativeAI(
            model=config.MODEL_NAME,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=config.TEMPERATURE
        )

        self.parser = PydanticOutputParser(pydantic_object=LessonPlan)
        self._setup_prompt()

    @staticmethod
    def clean_json_response(text: str) -> str:
        """Extract JSON from response, handling markdown code blocks"""
        text = text.strip()

        # Try to find JSON wrapped in markdown code blocks
        # Pattern: ```json ... ``` or ``` ... ```
        json_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        match = re.search(json_block_pattern, text, re.DOTALL)

        if match:
            return match.group(1).strip()

        # If no code blocks, try to find JSON object directly
        # Look for content between first { and last }
        json_pattern = r'(\{.*\})'
        match = re.search(json_pattern, text, re.DOTALL)

        if match:
            return match.group(1).strip()

        # If still nothing found, return the original text
        return text

    def _setup_prompt(self):
        """Setup the prompt template"""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert language teacher and curriculum designer.
Your task is to analyze a monologue in a foreign language and create a comprehensive lesson plan.

You should:
1. Identify the language and estimate the proficiency level
2. Extract 5-10 key vocabulary words that are important or challenging
3. Identify 3-5 important sentence structures or grammatical patterns
4. Create clear learning objectives
5. Generate 5-8 comprehension check questions to assess student understanding

For comprehension questions, create a mix of:
- Multiple choice questions (with 4 options each)
- True/False questions
- Fill-in-the-blank questions (testing vocabulary or grammar from the monologue)

Questions should test understanding of the monologue content, vocabulary usage, and grammatical structures.
Focus on words and structures that would be most valuable for language learners.

IMPORTANT: You MUST respond with valid JSON only. Do not include any additional text, explanations, or markdown formatting.
Your response should be a single JSON object that matches the schema exactly.

{format_instructions}"""),
            ("user", "Analyze this monologue and create a lesson plan. Respond with ONLY valid JSON:\n\n{monologue}")
        ])

    def generate_lesson_plan(self, monologue: str) -> LessonPlan:
        """
        Generate a lesson plan from a foreign language monologue.

        Args:
            monologue: The text of the monologue in a foreign language

        Returns:
            LessonPlan object with vocabulary, structures, and teaching suggestions
        """
        from langchain.output_parsers import OutputFixingParser

        try:
            # First attempt: generate and clean the output
            chain = self.prompt | self.llm

            response = chain.invoke({
                "monologue": monologue,
                "format_instructions": self.parser.get_format_instructions()
            })

            # Debug: print raw response
            print("=" * 80)
            print("RAW LLM RESPONSE:")
            print(response.content[:500])  # First 500 chars
            print("=" * 80)

            # Clean the response text
            cleaned_text = self.clean_json_response(response.content)

            # Debug: print cleaned response
            print("CLEANED JSON:")
            print(cleaned_text[:500])  # First 500 chars
            print("=" * 80)

            # Parse with the cleaned text
            result = self.parser.parse(cleaned_text)

            return result
        except Exception as e:
            # If parsing fails, try with OutputFixingParser which uses the LLM to fix the output
            print(f"Initial parsing failed: {e}. Attempting to fix output...")

            try:
                fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

                # Get the raw response again
                chain = self.prompt | self.llm
                response = chain.invoke({
                    "monologue": monologue,
                    "format_instructions": self.parser.get_format_instructions()
                })

                # Clean and fix
                cleaned_text = self.clean_json_response(response.content)
                result = fixing_parser.parse(cleaned_text)

                return result
            except Exception as e2:
                print(f"OutputFixingParser also failed: {e2}")
                raise Exception(f"Failed to generate valid lesson plan: {str(e2)}")

    def format_lesson_plan(self, lesson_plan: LessonPlan) -> str:
        """
        Format a lesson plan as readable text.

        Args:
            lesson_plan: The LessonPlan object to format

        Returns:
            Formatted string representation of the lesson plan
        """
        output = []
        output.append("=" * 80)
        output.append("LANGUAGE LEARNING LESSON PLAN")
        output.append("=" * 80)
        output.append(f"\nLanguage: {lesson_plan.detected_language}")
        output.append(f"Proficiency Level: {lesson_plan.proficiency_level}")
        output.append(f"\nSummary:\n{lesson_plan.summary}")

        output.append("\n" + "=" * 80)
        output.append("LEARNING OBJECTIVES")
        output.append("=" * 80)
        for i, objective in enumerate(lesson_plan.learning_objectives, 1):
            output.append(f"{i}. {objective}")

        output.append("\n" + "=" * 80)
        output.append("VOCABULARY WORDS")
        output.append("=" * 80)
        for i, word in enumerate(lesson_plan.vocabulary_words, 1):
            output.append(f"\n{i}. {word.word}")
            output.append(f"   Translation: {word.translation}")
            output.append(f"   Definition: {word.definition}")
            output.append(f"   Example: {word.example_sentence}")

        output.append("\n" + "=" * 80)
        output.append("SENTENCE STRUCTURES")
        output.append("=" * 80)
        for i, structure in enumerate(lesson_plan.sentence_structures, 1):
            output.append(f"\n{i}. {structure.structure_name}")
            output.append(f"   Explanation: {structure.explanation}")
            output.append(f"   Example from text: {structure.example_from_text}")
            output.append(f"   Practice template: {structure.practice_template}")

        output.append("\n" + "=" * 80)
        output.append("COMPREHENSION CHECKS")
        output.append("=" * 80)
        for i, question in enumerate(lesson_plan.comprehension_questions, 1):
            output.append(f"\n{i}. [{question.question_type.upper().replace('_', ' ')}] {question.question}")

            if question.question_type == "multiple_choice":
                for j, option in enumerate(question.options):
                    marker = "✓" if option == question.correct_answer else " "
                    output.append(f"   {chr(65+j)}) {option} {marker}")
            elif question.question_type == "true_false":
                output.append(f"   A) True {'✓' if question.correct_answer == 'True' else ''}")
                output.append(f"   B) False {'✓' if question.correct_answer == 'False' else ''}")
            elif question.question_type == "fill_blank":
                output.append(f"   Answer: {question.correct_answer}")

            output.append(f"   Explanation: {question.explanation}")

        output.append("\n" + "=" * 80)

        return "\n".join(output)

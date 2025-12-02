from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from config import config


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

{format_instructions}"""),
            ("user", "Analyze this monologue and create a lesson plan:\n\n{monologue}")
        ])

    def generate_lesson_plan(self, monologue: str) -> LessonPlan:
        """
        Generate a lesson plan from a foreign language monologue.

        Args:
            monologue: The text of the monologue in a foreign language

        Returns:
            LessonPlan object with vocabulary, structures, and teaching suggestions
        """
        chain = self.prompt | self.llm | self.parser

        result = chain.invoke({
            "monologue": monologue,
            "format_instructions": self.parser.get_format_instructions()
        })

        return result

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

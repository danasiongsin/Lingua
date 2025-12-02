# Language Learning Lesson Plan Agent

An AI-powered agent that analyzes foreign language monologues and generates comprehensive lesson plans. Built with LangChain and Google Gemini.

## Features

- **Automatic Language Detection**: Identifies the language of the input monologue
- **Proficiency Level Assessment**: Estimates the CEFR level (A1-C2)
- **Vocabulary Extraction**: Identifies key vocabulary words with translations and examples
- **Grammar Analysis**: Highlights important sentence structures and grammatical patterns
- **Learning Objectives**: Generates clear learning objectives for the lesson
- **Activity Suggestions**: Provides practical exercises for students to practice

## Setup

### 1. Install Dependencies

```bash
cd agent
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get a Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

### 3. Run the Agent

```bash
python main.py
```

## Usage

The main script provides several options:

1. **Use Spanish Example**: Pre-loaded Spanish monologue about daily routine
2. **Use French Example**: Pre-loaded French monologue about student life
3. **Enter Custom Monologue**: Type or paste your own monologue
4. **Load from File**: Read a monologue from a text file

### Example Usage

```bash
$ python main.py

Select an example or provide your own monologue:
1. Spanish example (daily routine)
2. French example (student life)
3. Enter custom monologue
4. Load from file

Enter your choice (1-4): 1
```

The agent will analyze the monologue and generate a detailed lesson plan including:
- Language and proficiency level
- Content summary
- Learning objectives
- Vocabulary words with translations and examples
- Sentence structures with explanations
- Suggested practice activities

## Using the Agent Programmatically

```python
from lesson_agent import LanguageLearningAgent

# Initialize the agent
agent = LanguageLearningAgent()

# Your monologue text
monologue = """
Bonjour! Je m'appelle Marie...
"""

# Generate lesson plan
lesson_plan = agent.generate_lesson_plan(monologue)

# Access structured data
print(f"Language: {lesson_plan.detected_language}")
print(f"Level: {lesson_plan.proficiency_level}")

for word in lesson_plan.vocabulary_words:
    print(f"{word.word}: {word.translation}")

# Or get formatted output
formatted = agent.format_lesson_plan(lesson_plan)
print(formatted)
```

## Output Format

The lesson plan includes:

### Lesson Plan Structure
```
LANGUAGE LEARNING LESSON PLAN
- Language: [Detected Language]
- Proficiency Level: [CEFR Level]
- Summary: [Content overview]

LEARNING OBJECTIVES
- [Objective 1]
- [Objective 2]
...

VOCABULARY WORDS
1. [word]
   Translation: [English translation]
   Definition: [Contextual definition]
   Example: [Example sentence]
...

SENTENCE STRUCTURES
1. [Structure name]
   Explanation: [How it works]
   Example from text: [Original example]
   Practice template: [Pattern to practice]
...

SUGGESTED ACTIVITIES
- [Activity 1]
- [Activity 2]
...
```

## Configuration Options

Edit the `.env` file to customize:

- `GOOGLE_API_KEY`: Your Google API key (required)
- `GEMINI_MODEL`: Model to use (default: `gemini-pro`)
- `TEMPERATURE`: Creativity level 0.0-1.0 (default: `0.7`)

## Architecture

- **lesson_agent.py**: Core LangChain agent implementation
  - `LanguageLearningAgent`: Main agent class
  - `LessonPlan`: Pydantic model for structured output
  - `VocabularyWord`: Model for vocabulary items
  - `SentenceStructure`: Model for grammar patterns

- **config.py**: Configuration management with environment variables
- **main.py**: CLI interface for running the agent

## Requirements

- Python 3.8+
- LangChain
- Google Generative AI (Gemini)
- Pydantic 2.0+

## Tips for Best Results

1. **Monologue Length**: 100-500 words works best
2. **Clear Context**: Monologues with clear themes produce better lesson plans
3. **Natural Language**: Real conversational text yields more useful vocabulary
4. **Variety**: Mix different tenses and structures for richer grammar analysis

## Troubleshooting

**Error: GOOGLE_API_KEY environment variable is required**
- Make sure you've created a `.env` file with your API key

**Error: API rate limit exceeded**
- Wait a moment and try again, or check your Google Cloud quota

**Poor quality output**
- Try adjusting the `TEMPERATURE` setting in `.env`
- Ensure the monologue is clear and well-structured

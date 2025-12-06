import { useState } from 'react'
import './App.css'
import Landing from "./Landing";
import LessonPage from './LessonPage';

interface LessonPlan {
  detected_language: string;
  proficiency_level: string;
  summary: string;
  vocabulary_words: Array<{
    word: string;
    translation: string;
    definition: string;
    example_sentence: string;
  }>;
  sentence_structures: Array<{
    structure_name: string;
    explanation: string;
    example_from_text: string;
    practice_template: string;
  }>;
  learning_objectives: string[];
  comprehension_questions: Array<{
    question: string;
    question_type: string;
    correct_answer: string;
    options: string[];
    explanation: string;
  }>;
}

interface ApiResponse {
  transcript: string;
  lesson_plan: LessonPlan;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ApiResponse | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!file) {
      setError('Please select a video file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('video', file);

    try {
      const response = await fetch('http://localhost:8000/llm/process-video', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process video');
      }

      const data: ApiResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const [selectedVideo, setSelectedVideo] = useState(null);

  // If no video picked → show landing page
  if (!selectedVideo) {
    return <Landing onSelectVideo={setSelectedVideo} />;
  }

  // Otherwise show main screen with chosen video
  return <LessonPage videoSrc={selectedVideo} />;
  return (
    <div className="App">
      <header className="App-header">
        <h1>Lingua - Language Learning Platform</h1>
        <p className="subtitle">Upload a video to generate a personalized lesson plan</p>
      </header>

      <main className="App-main">
        <div className="upload-section">
          <form onSubmit={handleSubmit} className="upload-form">
            <div className="file-input-wrapper">
              <label htmlFor="video-upload" className="file-label">
                {file ? file.name : 'Choose Video File'}
              </label>
              <input
                id="video-upload"
                type="file"
                accept="video/mp4,video/avi,video/mov,video/mkv,video/webm"
                onChange={handleFileChange}
                className="file-input"
              />
            </div>

            <button
              type="submit"
              disabled={!file || loading}
              className="submit-button"
            >
              {loading ? 'Processing...' : 'Generate Lesson Plan'}
            </button>
          </form>

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>

        {result && (
          <div className="results-section">
            <div className="result-card">
              <h2>Transcript</h2>
              <p className="transcript">{result.transcript}</p>
            </div>

            <div className="result-card">
              <h2>Lesson Plan</h2>

              <div className="lesson-header">
                <p><strong>Language:</strong> {result.lesson_plan.detected_language}</p>
                <p><strong>Proficiency Level:</strong> {result.lesson_plan.proficiency_level}</p>
              </div>

              <div className="lesson-section">
                <h3>Summary</h3>
                <p>{result.lesson_plan.summary}</p>
              </div>

              <div className="lesson-section">
                <h3>Learning Objectives</h3>
                <ul>
                  {result.lesson_plan.learning_objectives.map((obj, idx) => (
                    <li key={idx}>{obj}</li>
                  ))}
                </ul>
              </div>

              <div className="lesson-section">
                <h3>Vocabulary Words</h3>
                {result.lesson_plan.vocabulary_words.map((word, idx) => (
                  <div key={idx} className="vocabulary-item">
                    <h4>{word.word}</h4>
                    <p><strong>Translation:</strong> {word.translation}</p>
                    <p><strong>Definition:</strong> {word.definition}</p>
                    <p><em>Example: {word.example_sentence}</em></p>
                  </div>
                ))}
              </div>

              <div className="lesson-section">
                <h3>Sentence Structures</h3>
                {result.lesson_plan.sentence_structures.map((structure, idx) => (
                  <div key={idx} className="structure-item">
                    <h4>{structure.structure_name}</h4>
                    <p><strong>Explanation:</strong> {structure.explanation}</p>
                    <p><strong>Example:</strong> <em>{structure.example_from_text}</em></p>
                    <p><strong>Practice:</strong> {structure.practice_template}</p>
                  </div>
                ))}
              </div>

              <div className="lesson-section">
                <h3>Comprehension Questions</h3>
                {result.lesson_plan.comprehension_questions.map((q, idx) => (
                  <div key={idx} className="question-item">
                    <p className="question"><strong>Q{idx + 1}:</strong> {q.question}</p>
                    <p className="question-type">Type: {q.question_type.replace('_', ' ')}</p>

                    {q.options.length > 0 && (
                      <ul className="options">
                        {q.options.map((option, optIdx) => (
                          <li key={optIdx} className={option === q.correct_answer ? 'correct' : ''}>
                            {option} {option === q.correct_answer && '✓'}
                          </li>
                        ))}
                      </ul>
                    )}

                    {q.options.length === 0 && (
                      <p className="answer"><strong>Answer:</strong> {q.correct_answer}</p>
                    )}

                    <p className="explanation"><em>{q.explanation}</em></p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

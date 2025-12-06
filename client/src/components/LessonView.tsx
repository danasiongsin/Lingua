import React, { useState, useEffect } from 'react';
import './LessonView.css';

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

interface LessonViewProps {
  videoUrl: string;
  videoTitle: string;
  onBack: () => void;
}

const LessonView: React.FC<LessonViewProps> = ({ videoUrl, videoTitle, onBack }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'transcript' | 'vocabulary' | 'grammar' | 'quiz'>('transcript');

  useEffect(() => {
    const processVideo = async () => {
      setLoading(true);
      setError(null);

      try {
        // Fetch the video file from the public directory
        const videoResponse = await fetch(videoUrl);
        if (!videoResponse.ok) {
          throw new Error('Failed to load video file');
        }

        const videoBlob = await videoResponse.blob();
        const videoFile = new File([videoBlob], videoUrl.split('/').pop() || 'video.mp4', {
          type: videoBlob.type || 'video/mp4'
        });

        const formData = new FormData();
        formData.append('video', videoFile);

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

    processVideo();
  }, [videoUrl]);

  return (
    <div className="lesson-view">
      <div className="lesson-header">
        <button className="back-button" onClick={onBack}>
          ← Back to Videos
        </button>
        <h2 className="lesson-title">{videoTitle}</h2>
      </div>

      <div className="lesson-container">
        {/* Left side - Video Player */}
        <div className="video-section">
          <div className="video-player">
            <video controls src={videoUrl} className="video-element">
              Your browser does not support the video tag.
            </video>
          </div>

          {loading && (
            <div className="processing-status">
              <div className="spinner"></div>
              <p>Processing video and generating lesson plan...</p>
              <p className="status-detail">This may take a minute</p>
            </div>
          )}
        </div>

        {/* Right side - Lesson Content */}
        <div className="lesson-content">
          {error && (
            <div className="error-box">
              <strong>Error:</strong> {error}
            </div>
          )}

          {loading && !error && (
            <div className="loading-placeholder">
              <div className="pulse-box"></div>
              <div className="pulse-box"></div>
              <div className="pulse-box"></div>
            </div>
          )}

          {result && !loading && (
            <>
              <div className="lesson-info-bar">
                <span className="info-badge">
                  Language: {result.lesson_plan.detected_language}
                </span>
                <span className="info-badge">
                  Level: {result.lesson_plan.proficiency_level}
                </span>
              </div>

              <div className="tab-navigation">
                <button
                  className={`tab-button ${activeTab === 'transcript' ? 'active' : ''}`}
                  onClick={() => setActiveTab('transcript')}
                >
                  📝 Transcript
                </button>
                <button
                  className={`tab-button ${activeTab === 'vocabulary' ? 'active' : ''}`}
                  onClick={() => setActiveTab('vocabulary')}
                >
                  📚 Vocabulary
                </button>
                <button
                  className={`tab-button ${activeTab === 'grammar' ? 'active' : ''}`}
                  onClick={() => setActiveTab('grammar')}
                >
                  🎯 Grammar
                </button>
                <button
                  className={`tab-button ${activeTab === 'quiz' ? 'active' : ''}`}
                  onClick={() => setActiveTab('quiz')}
                >
                  ❓ Quiz
                </button>
              </div>

              <div className="tab-content">
                {activeTab === 'transcript' && (
                  <div className="content-section">
                    <h3>Transcript</h3>
                    <p className="transcript-text">{result.transcript}</p>

                    <h3 className="section-header">Summary</h3>
                    <p className="summary-text">{result.lesson_plan.summary}</p>

                    <h3 className="section-header">Learning Objectives</h3>
                    <ul className="objectives-list">
                      {result.lesson_plan.learning_objectives.map((obj, idx) => (
                        <li key={idx}>{obj}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {activeTab === 'vocabulary' && (
                  <div className="content-section">
                    <h3>Vocabulary Words</h3>
                    {result.lesson_plan.vocabulary_words.map((word, idx) => (
                      <div key={idx} className="vocab-card">
                        <h4 className="vocab-word">{word.word}</h4>
                        <p><strong>Translation:</strong> {word.translation}</p>
                        <p><strong>Definition:</strong> {word.definition}</p>
                        <p className="vocab-example"><em>"{word.example_sentence}"</em></p>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'grammar' && (
                  <div className="content-section">
                    <h3>Sentence Structures</h3>
                    {result.lesson_plan.sentence_structures.map((structure, idx) => (
                      <div key={idx} className="grammar-card">
                        <h4 className="grammar-title">{structure.structure_name}</h4>
                        <p><strong>Explanation:</strong> {structure.explanation}</p>
                        <p><strong>Example from video:</strong> <em>"{structure.example_from_text}"</em></p>
                        <p className="practice-template">
                          <strong>Practice:</strong> {structure.practice_template}
                        </p>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'quiz' && (
                  <div className="content-section">
                    <h3>Comprehension Questions</h3>
                    {result.lesson_plan.comprehension_questions.map((q, idx) => (
                      <div key={idx} className="quiz-card">
                        <p className="quiz-question">
                          <strong>Question {idx + 1}:</strong> {q.question}
                        </p>
                        <p className="quiz-type">Type: {q.question_type.replace('_', ' ')}</p>

                        {q.options.length > 0 && (
                          <ul className="quiz-options">
                            {q.options.map((option, optIdx) => (
                              <li
                                key={optIdx}
                                className={option === q.correct_answer ? 'correct-option' : ''}
                              >
                                {option} {option === q.correct_answer && '✓'}
                              </li>
                            ))}
                          </ul>
                        )}

                        {q.options.length === 0 && (
                          <p className="quiz-answer">
                            <strong>Answer:</strong> {q.correct_answer}
                          </p>
                        )}

                        <p className="quiz-explanation">{q.explanation}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default LessonView;

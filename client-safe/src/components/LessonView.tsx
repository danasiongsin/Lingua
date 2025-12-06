import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
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
  const [revealedAnswers, setRevealedAnswers] = useState<Set<number>>(new Set());
  const [selectedAnswers, setSelectedAnswers] = useState<Map<number, string>>(new Map());
  const [vocabExamples, setVocabExamples] = useState<Map<number, { description: string; examples: string[] }>>(new Map());
  const [grammarExamples, setGrammarExamples] = useState<Map<number, { description: string; examples: string[] }>>(new Map());
  const [loadingExamples, setLoadingExamples] = useState<Set<string>>(new Set());
  const videoRef = React.useRef<HTMLVideoElement>(null);

  const handleAnswerSelect = (questionIndex: number, selectedOption: string) => {
    setSelectedAnswers(prev => {
      const newMap = new Map(prev);
      newMap.set(questionIndex, selectedOption);
      return newMap;
    });
    // Auto-reveal the answer when user selects
    setRevealedAnswers(prev => {
      const newSet = new Set(prev);
      newSet.add(questionIndex);
      return newSet;
    });
  };

  const fetchMoreExamples = async (type: 'vocab' | 'grammar', index: number, item: any) => {
    const key = `${type}-${index}`;
    setLoadingExamples(prev => new Set(prev).add(key));

    try {
      const requestBody = type === 'vocab'
        ? {
            item_type: 'vocab',
            word: item.word,
            translation: item.translation
          }
        : {
            item_type: 'grammar',
            structure_name: item.structure_name
          };

      const response = await fetch('http://localhost:8000/llm/generate-examples', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch examples');
      }

      const data = await response.json();
      const result = {
        description: data.description || '',
        examples: data.examples || []
      };

      if (type === 'vocab') {
        setVocabExamples(prev => {
          const newMap = new Map(prev);
          newMap.set(index, result);
          return newMap;
        });
      } else {
        setGrammarExamples(prev => {
          const newMap = new Map(prev);
          newMap.set(index, result);
          return newMap;
        });
      }
    } catch (err) {
      console.error('Error fetching examples:', err);
    } finally {
      setLoadingExamples(prev => {
        const newSet = new Set(prev);
        newSet.delete(key);
        return newSet;
      });
    }
  };

  useEffect(() => {
    // Auto-play the video when component mounts
    if (videoRef.current) {
      // Try to play with sound first
      videoRef.current.muted = false;
      videoRef.current.play().catch(error => {
        console.log('Auto-play with sound failed, trying muted:', error);
        // If auto-play fails, try muted (browsers often require muted for auto-play)
        if (videoRef.current) {
          videoRef.current.muted = true;
          videoRef.current.play().catch(err => {
            console.log('Muted auto-play also failed:', err);
          });
        }
      });
    }

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
            <video
              ref={videoRef}
              controls
              src={videoUrl}
              className="video-element"
            >
              Your browser does not support the video tag.
            </video>
          </div>

          {loading && (
            <div className="processing-status">
              <div className="spinner"></div>
              <p>Processing video and generating lesson plan...</p>
              <p className="status-detail">Video is playing while we prepare your lesson</p>
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
              <div className="loading-message">
                <div className="spinner-large"></div>
                <h3>Generating Your Lesson...</h3>
                <p>Analyzing the video content and creating a personalized learning experience.</p>
                <p className="tip">Watch the video while you wait!</p>
              </div>
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
                    {result.lesson_plan.vocabulary_words.map((word, idx) => {
                      const examples = vocabExamples.get(idx);
                      const isLoading = loadingExamples.has(`vocab-${idx}`);

                      return (
                        <div key={idx} className="vocab-card">
                          <div className="card-header">
                            <h4 className="vocab-word">{word.word}</h4>
                            <button
                              className="more-info-button"
                              onClick={() => fetchMoreExamples('vocab', idx, word)}
                              disabled={isLoading || examples !== undefined}
                              title="Get more examples"
                            >
                              {isLoading ? '⏳' : examples ? '✓' : 'ℹ️'}
                            </button>
                          </div>
                          <p><strong>Translation:</strong> {word.translation}</p>
                          <p><strong>Definition:</strong> {word.definition}</p>
                          <p className="vocab-example"><em>"{word.example_sentence}"</em></p>

                          {isLoading && (
                            <div className="loading-examples">
                              <p>Loading more examples...</p>
                            </div>
                          )}

                          {examples && (
                            <div className="additional-examples">
                              <div className="detailed-description">
                                <p><strong>In-Depth Analysis:</strong></p>
                                <ReactMarkdown>{examples.description}</ReactMarkdown>
                              </div>
                              <div className="examples-list">
                                <p><strong>Additional Examples:</strong></p>
                                {examples.examples.map((ex, i) => (
                                  <div key={i} className="example-item">
                                    <ReactMarkdown>{ex}</ReactMarkdown>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}

                {activeTab === 'grammar' && (
                  <div className="content-section">
                    <h3>Sentence Structures</h3>
                    {result.lesson_plan.sentence_structures.map((structure, idx) => {
                      const examples = grammarExamples.get(idx);
                      const isLoading = loadingExamples.has(`grammar-${idx}`);

                      return (
                        <div key={idx} className="grammar-card">
                          <div className="card-header">
                            <h4 className="grammar-title">{structure.structure_name}</h4>
                            <button
                              className="more-info-button"
                              onClick={() => fetchMoreExamples('grammar', idx, structure)}
                              disabled={isLoading || examples !== undefined}
                              title="Get more examples"
                            >
                              {isLoading ? '⏳' : examples ? '✓' : 'ℹ️'}
                            </button>
                          </div>
                          <p><strong>Explanation:</strong> {structure.explanation}</p>
                          <p><strong>Example from video:</strong> <em>"{structure.example_from_text}"</em></p>
                          <p className="practice-template">
                            <strong>Practice:</strong> {structure.practice_template}
                          </p>

                          {isLoading && (
                            <div className="loading-examples">
                              <p>Loading more examples...</p>
                            </div>
                          )}

                          {examples && (
                            <div className="additional-examples">
                              <div className="detailed-description">
                                <p><strong>In-Depth Analysis:</strong></p>
                                <ReactMarkdown>{examples.description}</ReactMarkdown>
                              </div>
                              <p><strong>Additional Examples:</strong></p>
                              <ul>
                                {examples.examples.map((ex, i) => (
                                  <li key={i}><em>"{ex}"</em></li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}

                {activeTab === 'quiz' && (
                  <div className="content-section">
                    <h3>Comprehension Questions</h3>
                    {result.lesson_plan.comprehension_questions.map((q, idx) => {
                      const isRevealed = revealedAnswers.has(idx);
                      const selectedAnswer = selectedAnswers.get(idx);
                      const isAnswered = selectedAnswer !== undefined;

                      return (
                        <div key={idx} className="quiz-card">
                          <p className="quiz-question">
                            <strong>Question {idx + 1}:</strong> {q.question}
                          </p>
                          <p className="quiz-type">Type: {q.question_type.replace('_', ' ')}</p>

                          {q.options.length > 0 && (
                            <ul className="quiz-options">
                              {q.options.map((option, optIdx) => {
                                const isCorrect = option === q.correct_answer;
                                const isSelected = selectedAnswer === option;
                                let className = 'quiz-option';

                                if (isRevealed) {
                                  if (isCorrect) {
                                    className += ' correct-option';
                                  } else if (isSelected && !isCorrect) {
                                    className += ' incorrect-option';
                                  }
                                } else if (isSelected) {
                                  className += ' selected-option';
                                }

                                return (
                                  <li
                                    key={optIdx}
                                    className={className}
                                    onClick={() => !isRevealed && handleAnswerSelect(idx, option)}
                                    style={{ cursor: isRevealed ? 'default' : 'pointer' }}
                                  >
                                    {option}
                                    {isRevealed && isCorrect && ' ✓'}
                                    {isRevealed && isSelected && !isCorrect && ' ✗'}
                                  </li>
                                );
                              })}
                            </ul>
                          )}

                          {q.options.length === 0 && (
                            <div className="text-answer-input">
                              <input
                                type="text"
                                placeholder="Type your answer here..."
                                value={selectedAnswer || ''}
                                onChange={(e) => {
                                  const newMap = new Map(selectedAnswers);
                                  newMap.set(idx, e.target.value);
                                  setSelectedAnswers(newMap);
                                }}
                                className="answer-input-field"
                                disabled={isRevealed}
                              />
                              {!isRevealed && selectedAnswer && (
                                <button
                                  className="submit-answer-button"
                                  onClick={() => {
                                    setRevealedAnswers(prev => {
                                      const newSet = new Set(prev);
                                      newSet.add(idx);
                                      return newSet;
                                    });
                                  }}
                                >
                                  Submit Answer
                                </button>
                              )}
                            </div>
                          )}

                          {isRevealed && (
                            <>
                              {q.options.length === 0 && (
                                <>
                                  <p className="quiz-answer">
                                    <strong>Correct Answer:</strong> {q.correct_answer}
                                  </p>
                                  {selectedAnswer && (
                                    <p className={selectedAnswer.toLowerCase().trim() === q.correct_answer.toLowerCase().trim() ? 'feedback-correct' : 'feedback-incorrect'}>
                                      {selectedAnswer.toLowerCase().trim() === q.correct_answer.toLowerCase().trim()
                                        ? '✓ Correct!'
                                        : `✗ Your answer: "${selectedAnswer}"`}
                                    </p>
                                  )}
                                </>
                              )}
                              {q.options.length > 0 && isAnswered && (
                                <p className={selectedAnswer === q.correct_answer ? 'feedback-correct' : 'feedback-incorrect'}>
                                  {selectedAnswer === q.correct_answer ? '✓ Correct!' : '✗ Incorrect. Try again!'}
                                </p>
                              )}
                              <p className="quiz-explanation">{q.explanation}</p>
                            </>
                          )}
                        </div>
                      );
                    })}
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

import React from 'react';
import './WelcomePage.css';

interface SampleVideo {
  id: string;
  title: string;
  language: string;
  thumbnail: string;
  videoUrl: string;
  flag: string;
}

interface WelcomePageProps {
  onVideoSelect: (video: SampleVideo) => void;
}

const sampleVideos: SampleVideo[] = [
  {
    id: 'english',
    title: 'English Conversation',
    language: 'English',
    thumbnail: '🇺🇸',
    videoUrl: '/videos/english-sample.mp4',
    flag: '🇺🇸'
  },
  {
    id: 'spanish',
    title: 'Spanish Lesson',
    language: 'Spanish',
    thumbnail: '🇪🇸',
    videoUrl: '/videos/spanish-sample.mp4',
    flag: '🇪🇸'
  },
  {
    id: 'french',
    title: 'French Tutorial',
    language: 'French',
    thumbnail: '🇫🇷',
    videoUrl: '/videos/french-sample.mp4',
    flag: '🇫🇷'
  }
];

const WelcomePage: React.FC<WelcomePageProps> = ({ onVideoSelect }) => {
  return (
    <div className="welcome-page">
      <div className="welcome-header">
        <h1 className="welcome-title">Welcome to Lingua</h1>
        <p className="welcome-subtitle">Learn languages through immersive video content</p>
        <p className="welcome-description">
          Select a sample video to begin your learning journey. Our AI will analyze the content
          and create a personalized lesson plan just for you.
        </p>
      </div>

      <div className="video-grid">
        {sampleVideos.map((video) => (
          <div
            key={video.id}
            className="video-card"
            onClick={() => onVideoSelect(video)}
          >
            <div className="video-thumbnail">
              <span className="video-flag">{video.flag}</span>
            </div>
            <div className="video-info">
              <h3 className="video-title">{video.title}</h3>
              <p className="video-language">{video.language}</p>
              <button className="select-button">
                Start Learning
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="features-section">
        <h2>What You'll Get</h2>
        <div className="features-grid">
          <div className="feature">
            <span className="feature-icon">📝</span>
            <h3>Transcripts</h3>
            <p>Complete text transcription of the video</p>
          </div>
          <div className="feature">
            <span className="feature-icon">📚</span>
            <h3>Vocabulary</h3>
            <p>Key words with translations and examples</p>
          </div>
          <div className="feature">
            <span className="feature-icon">🎯</span>
            <h3>Grammar</h3>
            <p>Sentence structures and practice templates</p>
          </div>
          <div className="feature">
            <span className="feature-icon">❓</span>
            <h3>Quizzes</h3>
            <p>Comprehension questions to test your understanding</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomePage;
export type { SampleVideo };

import { useState } from 'react';
import './App.css';
import WelcomePage from './components/WelcomePage';
import LessonView from './components/LessonView';
import type { SampleVideo } from './components/WelcomePage';

function App() {
  const [selectedVideo, setSelectedVideo] = useState<SampleVideo | null>(null);

  const handleVideoSelect = (video: SampleVideo) => {
    setSelectedVideo(video);
  };

  const handleBackToWelcome = () => {
    setSelectedVideo(null);
  };

  return (
    <div className="App">
      {!selectedVideo ? (
        <WelcomePage onVideoSelect={handleVideoSelect} />
      ) : (
        <LessonView
          videoUrl={selectedVideo.videoUrl}
          videoTitle={selectedVideo.title}
          onBack={handleBackToWelcome}
        />
      )}
    </div>
  );
}

export default App;

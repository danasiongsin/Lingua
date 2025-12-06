import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import Landing from "./Landing";
import LessonPage from './LessonPage';

function App() {

  const [selectedVideo, setSelectedVideo] = useState(null);

  // If no video picked → show landing page
  if (!selectedVideo) {
    return <Landing onSelectVideo={setSelectedVideo} />;
  }

  // Otherwise show main screen with chosen video
  return <LessonPage videoSrc={selectedVideo} />;
}

export default App

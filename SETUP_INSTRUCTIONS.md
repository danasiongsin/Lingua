# Lingua Frontend Setup Instructions

## Overview
The frontend has been implemented with the following features:
- Welcome page with 3 sample video selections (English, Spanish, French)
- Video player that plays while the backend processes the video
- Side-by-side layout with video on the left and lesson content on the right
- Tabbed interface for organizing lesson content (Transcript, Vocabulary, Grammar, Quiz)

## Project Structure

```
client-safe/                      # PRIMARY FRONTEND
├── src/
│   ├── components/
│   │   ├── WelcomePage.tsx       # Landing page with video selection
│   │   ├── WelcomePage.css       # Styling for welcome page
│   │   ├── LessonView.tsx        # Main lesson view with video + content
│   │   └── LessonView.css        # Styling for lesson view
│   ├── App.tsx                   # Main app component (navigation)
│   └── App.css                   # Global app styles
└── public/
    └── videos/
        ├── README.md
        ├── english-sample.mp4    # (You need to add this)
        ├── spanish-sample.mp4    # (You need to add this)
        └── french-sample.mp4     # (You need to add this)
```

## Setup Steps

### 1. Add Sample Videos
Place your sample video files in `client-safe/public/videos/` with these exact names:
- `english-sample.mp4`
- `spanish-sample.mp4`
- `french-sample.mp4`

**Requirements:**
- Format: MP4 (or other browser-supported formats)
- Recommended length: 1-5 minutes
- Should contain clear spoken content in the target language

**Quick tip:** You can find royalty-free language learning videos on:
- YouTube (download with youtube-dl or similar)
- Pexels (videos with voiceovers)
- Your own recordings

### 2. Install Dependencies
```bash
cd client-safe
npm install
```

### 3. Start the Backend
Make sure your FastAPI backend is running:
```bash
cd server
export LLM_API_KEY="your-api-key-here"
uvicorn main:app --reload --port 8000
```

### 4. Start the Frontend
```bash
cd client-safe
npm run dev
```

The app will open at `http://localhost:5173` (Vite default port)

## How It Works

1. **Welcome Page:**
   - Users see three sample video cards (English, Spanish, French)
   - Each card displays a flag emoji and language information
   - Clicking "Start Learning" selects that video

2. **Lesson View:**
   - **Left Side:** Video player that displays and plays the selected video
   - **Right Side:** Lesson content organized in tabs
     - **Transcript Tab:** Full transcript, summary, and learning objectives
     - **Vocabulary Tab:** Key words with translations, definitions, and examples
     - **Grammar Tab:** Sentence structures with explanations and practice templates
     - **Quiz Tab:** Comprehension questions with answers and explanations

3. **Processing Flow:**
   - When a video is selected, it starts playing immediately
   - Simultaneously, the video is sent to the backend for processing
   - A loading indicator shows "Processing video and generating lesson plan..."
   - Once complete, the lesson content populates on the right side
   - Users can switch between tabs to explore different aspects of the lesson

## Features

- **Responsive Design:** Works on desktop and mobile devices
- **Beautiful UI:** Gradient backgrounds, smooth animations, and modern styling
- **Real-time Processing:** Video plays while the backend generates the lesson
- **Organized Content:** Tabbed interface keeps lesson material well-structured
- **Easy Navigation:** "Back to Videos" button returns to the welcome page

## Troubleshooting

### Videos won't play
- Ensure video files are in the correct location: `client-safe/public/videos/`
- Check that video files are named exactly: `english-sample.mp4`, `spanish-sample.mp4`, `french-sample.mp4`
- Try using MP4 format for best browser compatibility

### Backend connection fails
- Verify the backend is running on `http://localhost:8000`
- Check that the LLM_API_KEY environment variable is set
- Ensure CORS is enabled on the backend (FastAPI should handle this automatically)

### Lesson content doesn't load
- Check browser console for errors (F12 → Console tab)
- Verify the backend endpoint `/llm/process-video` is working
- Test the backend directly with a curl command or Postman

## Next Steps

You can enhance the application by:
- Adding user authentication to save progress
- Implementing a quiz interaction system (click to reveal answers)
- Adding pronunciation guides with audio
- Creating a "My Lessons" section to track completed videos
- Supporting custom video uploads
- Adding subtitles/captions to the video player

# Lingua - Language Learning Platform

Learn languages through immersive video content with AI-generated lesson plans.

## Features

- **Sample Video Library**: Choose from English, Spanish, or French sample videos to start learning
- **AI-Powered Lesson Generation**: Automatically generates comprehensive lesson plans from video content
- **Interactive Video Player**: Watch videos while the AI processes and creates your personalized lesson
- **Organized Learning Content**:
  - Full transcripts with summaries
  - Vocabulary words with translations and examples
  - Grammar structures and practice templates
  - Comprehension quizzes with explanations
- **Beautiful UI**: Modern, responsive design that works on desktop and mobile

## Quick Start

### Prerequisites
- Node.js (for frontend)
- Python 3.8+ (for backend)
- LLM API key (for AI processing)

### 1. Add Sample Videos
Place video files in `client-safe/public/videos/`:
- `english-sample.mp4`
- `spanish-sample.mp4`
- `french-sample.mp4`

### 2. Install Dependencies

**Backend:**
```bash
cd server
pip install -r requirements.txt
```

**Frontend:**
```bash
cd client-safe
npm install
```

### 3. Set Environment Variables
```bash
export LLM_API_KEY="your-api-key-here"
```

### 4. Start Development Servers

**Option A: Use the startup script (recommended)**
```bash
./start-dev.sh
```

**Option B: Start manually**

Terminal 1 (Backend):
```bash
cd server
uvicorn main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd client-safe
npm run dev
```

### 5. Open the Application
Navigate to `http://localhost:5173` in your browser

## Project Structure

```
Lingua/
├── client-safe/               # PRIMARY FRONTEND - React with Vite
│   ├── src/
│   │   ├── components/
│   │   │   ├── WelcomePage.tsx    # Video selection page
│   │   │   ├── WelcomePage.css
│   │   │   ├── LessonView.tsx     # Main lesson interface
│   │   │   └── LessonView.css
│   │   ├── App.tsx            # Main app component
│   │   └── App.css
│   └── public/
│       └── videos/            # Sample video files go here
│
├── client/                    # Legacy frontend (for reference)
│
├── server/                    # FastAPI backend
│   ├── main.py               # FastAPI app entry point
│   ├── routers/              # API route handlers
│   ├── services/             # Business logic
│   └── config.py             # Configuration management
│
├── SETUP_INSTRUCTIONS.md     # Detailed setup guide
└── start-dev.sh              # Development startup script
```

## How It Works

1. User selects a sample video from the welcome page
2. Video begins playing immediately
3. Frontend sends the video to the backend for processing
4. Backend uses AI to:
   - Transcribe the audio
   - Detect the language
   - Generate vocabulary lists
   - Create grammar explanations
   - Develop comprehension questions
5. Lesson content appears in a tabbed interface next to the video

## Documentation

- [Detailed Setup Instructions](SETUP_INSTRUCTIONS.md)
- [Claude Code Guide](CLAUDE.md) - For AI assistant integration

## Technologies

**Frontend:**
- React 19
- TypeScript
- Vite (build tool and dev server)
- CSS3 with gradients and animations

**Backend:**
- FastAPI
- Python 3.8+
- Async/await patterns
- LLM integration for AI processing

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License
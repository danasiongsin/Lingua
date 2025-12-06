# Google Cloud Speech-to-Text Setup Guide

This guide walks you through setting up Google Cloud credentials for the video transcription feature.

## Prerequisites

- A Google Cloud account
- A project created in Google Cloud Console

## Step-by-Step Setup

### 1. Enable the Speech-to-Text API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **APIs & Services** → **Library**
4. Search for "Cloud Speech-to-Text API"
5. Click on it and click **Enable**

### 2. Create a Service Account

1. In the Google Cloud Console, go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Fill in the details:
   - **Service account name**: `lingua-speech-service` (or your preferred name)
   - **Service account description**: "Service account for Speech-to-Text API"
4. Click **Create and Continue**
5. Grant the role: **Cloud Speech Client** or **Cloud Speech-to-Text API User**
6. Click **Continue**, then **Done**

### 3. Create and Download Service Account Key

1. In the **Service Accounts** page, find your newly created service account
2. Click the three dots (⋮) on the right side
3. Select **Manage keys**
4. Click **Add Key** → **Create new key**
5. Choose **JSON** format
6. Click **Create**
7. A JSON file will be downloaded to your computer - **keep this file secure!**

### 4. Configure Your Local Environment

#### Option A: Using a credentials file (Recommended for development)

1. Move the downloaded JSON file to your server directory:
   ```bash
   mv ~/Downloads/your-service-account-key.json /path/to/Lingua/server/google-credentials.json
   ```

2. Create a `.env` file in the server directory (copy from `.env.example`):
   ```bash
   cd server
   cp .env.example .env
   ```

3. Edit `.env` and set the path to your credentials file:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/Lingua/server/google-credentials.json
   ```

4. Restart your FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

#### Option B: Using environment variable

Alternatively, you can set the environment variable directly in your shell:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/google-credentials.json"
export LLM_API_KEY="your-llm-api-key"
uvicorn main:app --reload --port 8000
```

### 5. Verify Setup

Test the endpoint with a video file:

```bash
curl -X POST "http://localhost:8000/llm/process-video" \
  -F "video=@/path/to/your/video.mp4"
```

If configured correctly, you should receive a JSON response with:
- `transcript`: The transcribed text from the video
- `ai_response`: The AI agent's response to the transcript

## Troubleshooting

### Error: "Could not automatically determine credentials"

- Make sure `GOOGLE_APPLICATION_CREDENTIALS` is set to the absolute path of your JSON key file
- Verify the path is correct and the file exists
- Restart your server after setting the environment variable

### Error: "Permission denied"

- Verify your service account has the "Cloud Speech Client" role
- Check that the Speech-to-Text API is enabled for your project

### Error: "Invalid credentials"

- Make sure you downloaded the JSON key file correctly
- Don't edit the JSON file manually
- Try creating a new service account key

## Security Best Practices

1. **Never commit credentials to git** - The `.gitignore` file is configured to exclude credential files
2. **Use different service accounts for production and development**
3. **Regularly rotate service account keys**
4. **Set appropriate IAM roles** - Only grant the minimum permissions needed
5. **Monitor API usage** in the Google Cloud Console

## Supported Audio Formats

The service currently processes these video formats:
- MP4
- AVI
- MOV
- MKV
- WEBM

Audio is automatically extracted and converted to WAV format before transcription.

## API Limits and Quotas

Google Cloud Speech-to-Text has usage limits. Check your quotas at:
[Google Cloud Console → APIs & Services → Quotas](https://console.cloud.google.com/apis/api/speech.googleapis.com/quotas)

For pricing information, visit:
https://cloud.google.com/speech-to-text/pricing

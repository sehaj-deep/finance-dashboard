# Setup Guide

## 1. Install Python
Since you are on Windows, the easiest way is:

1.  **Download**: Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version (e.g., Python 3.12).
2.  **Run Installer**: Run the executable.
3.  **CRITICAL STEP**: On the first screen, **Check the box that says "Add python.exe to PATH"**.
    - *If you miss this, the command line won't find Python.*
4.  **Finish**: Click "Install Now".
5.  **Verify**: Open a *new* terminal (Command Prompt or PowerShell) and type `python --version`. It should show `Python 3.12.x`.

## 2. Get Gemini API Key
Your "Gemini Advanced" subscription is for the *Chat Interface* (gemini.google.com). For code/apps, you need an **API Key** from Google AI Studio.

1.  **Go to**: [Google AI Studio](https://aistudio.google.com/app/apikey)
2.  **Sign In**: Use your Google account.
3.  **Create Key**: Click **"Create API Key"**.
    - You can create it in a new project or an existing one.
4.  **Copy**: Copy the string (starts with `AIza...`).
5.  **Paste**:
    - Open the file `d:\Coding\Vibe_Coding\finance_app\backend\.env.example` in VS Code.
    - Paste your key: `GEMINI_API_KEY=AIzaSyD...`
    - **Rename** the file from `.env.example` to just `.env`.

### Does "Pro" change anything?
- **Not directly for the API**: The API has a generous **Free Tier** (Gemini 1.5 Flash) which is perfect for this app.
- **Limits**: The free tier has rate limits (e.g., 15 requests/minute), which is plenty for personal use.
- **Persistence**: Yes, this API Key remains active indefinitely unless you delete it or your project is suspended. You don't need a new one every time.

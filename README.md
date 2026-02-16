# 💰 Personal Finance Dashboard

A privacy-focused, AI-powered personal finance dashboard that categorizes your bank transactions automatically using **Groq (Llama 3)**.

## ✨ Features

-   **AI Categorization**: Automatically categorizes transactions (Food, Rent, Transport, etc.) using Llama 3 on Groq.
-   **Privacy First**: Your data stays local (SQLite). Only sanitized transaction descriptions are sent to the AI.
-   **Smart Learning**: If you correct a category, the system "learns" and applies it to future transactions.
-   **Visual Dashboard**: View spending breakdowns and trends.
-   **PDF Support**: Drag-and-drop support for bank statements (optimized for CIBC but adaptable).

## 🚀 Getting Started

### Prerequisites

-   **Python 3.10+**
-   **Node.js 16+**
-   **Groq API Key** (Free at [console.groq.com](https://console.groq.com))

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```ini
GROQ_API_KEY=gsk_your_key_here
```

Run the server:
```bash
python -m uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit **http://localhost:5173** to use the app!

## 🛠️ Tech Stack

-   **Frontend**: Vue 3 + Vite
-   **Backend**: FastAPI (Python)
-   **Database**: SQLite + SQLAlchemy
-   **AI**: Groq API (Llama 3.3 70B)

## ⚠️ Important Note on Privacy

This application is designed to run locally.
-   **PDFs are processed locally.**
-   **No bank credentials are required.**
-   **Only transaction text** is sent to the AI provider. Account numbers and dates are stripped before sending.

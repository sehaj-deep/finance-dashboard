# Finance Dashboard - Architecture Documentation

## System Overview
Your Personal Finance Dashboard is a **privacy-first** web application that categorizes bank transactions using AI while keeping all sensitive data local.

## Tech Stack
- **Frontend**: Vue.js 3 + Vite (running on `http://localhost:5174`)
- **Backend**: Python FastAPI (running on `http://localhost:8000`)
- **Database**: SQLite (local file at `data/finance.db`)
- **AI**: Google Gemini 1.5 Flash (Free Tier)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                    http://localhost:5174                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │   Upload     │  │ Transactions │         │
│  │   (Charts)   │  │  (PDF/CSV)   │  │    (List)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP Requests (via Vite Proxy)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│                   http://localhost:8000                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  main.py (API Endpoints)                                 │  │
│  │  • POST /upload  → Accepts PDF/CSV                       │  │
│  │  • GET /transactions → Returns all transactions          │  │
│  │  • GET /summary → Stats for dashboard                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ingest.py (File Parsing)                                │  │
│  │  • parse_pdf() → Extracts text from PDF                  │  │
│  │  • parse_csv() → Parses CSV files                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  categorizer.py (AI Logic)                               │  │
│  │  1. sanitize() → STRIPS sensitive data                   │  │
│  │  2. predict_category() → Calls Gemini API                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  database.py (SQLite ORM)                                │  │
│  │  • Transactions Table                                    │  │
│  │  • Categories Table                                      │  │
│  │  • CategoryRules Table (Learning)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Only SANITIZED text
                            ▼
                   ┌─────────────────┐
                   │  Gemini API     │
                   │  (Cloud)        │
                   └─────────────────┘
```

---

## Data Flow: Upload to Dashboard

### Step 1: User Uploads PDF
```
User → Frontend (Upload.vue) → Backend (/upload endpoint)
```

### Step 2: PDF Parsing
```python
# ingest.py extracts:
{
  "date": "01/15/2026",
  "description": "STARBUCKS STORE #1234 REF:98765",
  "amount": 5.40
}
```

### Step 3: Privacy Sanitization
```python
# categorizer.py sanitizes BEFORE sending to Gemini:
Original: "STARBUCKS STORE #1234 REF:98765 01/15/2026 $5.40"
Sanitized: "STARBUCKS STORE [ACC#] REF:[ACC#] [DATE] [AMT]"
```

### Step 4: AI Categorization
```
Backend → Gemini API (receives: "STARBUCKS STORE")
Gemini → Backend (returns: "Food")
```

### Step 5: Database Storage
```sql
INSERT INTO transactions (date, description, amount, category)
VALUES ('01/15/2026', 'STARBUCKS STORE #1234', 5.40, 'Food')
```

### Step 6: Dashboard Display
```
Backend → Frontend (JSON response)
Frontend → Renders charts with FULL data (amounts, dates)
```

---

## Privacy Guarantees

### What Gemini NEVER Sees:
- ❌ Transaction amounts ($5.40)
- ❌ Dates (01/15/2026)
- ❌ Account numbers (98765)
- ❌ Your name, address, or bank details

### What Gemini DOES See:
- ✅ Merchant name only ("STARBUCKS STORE")

### Verification:
You can check the sanitization by looking at the backend logs when a transaction is processed. The log will show the exact string sent to Gemini.

---

## Learning System

### How It Works:
1. **First Time**: "STARBUCKS" → Gemini → "Food"
2. **You Correct**: User changes "Food" to "Entertainment" in UI
3. **Backend Saves Rule**: `CategoryRules` table stores `keyword="STARBUCKS", category="Entertainment"`
4. **Next Time**: "STARBUCKS" → **Skips Gemini** → Returns "Entertainment" instantly

This means:
- Faster categorization over time
- No API calls for repeated merchants
- Your corrections are remembered

---

## Database Schema

### `transactions` Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| date | String | Transaction date |
| description | String | Full merchant description |
| amount | Float | Transaction amount |
| category | String | Assigned category |

### `categories` Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String | Category name (e.g., "Food") |
| type | String | "Expense" or "Income" |

### `category_rules` Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| keyword | String | Merchant keyword |
| category | String | Assigned category |

---

## API Endpoints

### `POST /upload`
**Purpose**: Upload PDF or CSV bank statement

**Request**:
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@statement.pdf"
```

**Response**:
```json
{
  "filename": "statement.pdf",
  "transactions_processed": 45,
  "new_saved": 12
}
```

### `GET /transactions`
**Purpose**: Retrieve all transactions

**Response**:
```json
[
  {
    "id": 1,
    "date": "01/15/2026",
    "description": "STARBUCKS STORE",
    "amount": 5.40,
    "category": "Food"
  }
]
```

### `GET /summary`
**Purpose**: Get dashboard statistics (To be implemented)

---

## Current Status

### ✅ Completed:
- Backend API running on port 8000
- Frontend dev server running on port 5174
- Database initialized with 10 default categories
- Gemini API configured with your key
- Privacy sanitization layer active
- PDF parsing logic implemented

### 🚧 Next Steps:
- Build Vue.js frontend components (Dashboard, Upload, Transactions)
- Implement drag-and-drop file upload
- Create charts for spending visualization
- Add manual category correction UI
- Test with a real bank statement PDF

---

## File Structure
```
finance_app/
├── backend/
│   ├── main.py           # FastAPI app & endpoints
│   ├── database.py       # SQLite models
│   ├── ingest.py         # PDF/CSV parsing
│   ├── categorizer.py    # AI + Sanitization
│   ├── .env              # Your API key (NEVER commit!)
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # Vue components (to be built)
│   │   └── App.vue       # Main app
│   ├── vite.config.js    # Proxy to backend
│   └── package.json
└── data/
    └── finance.db        # SQLite database (auto-created)
```

---

## Security Notes

1. **API Key**: Your Gemini key is in `.env` and loaded via `dotenv`. Never commit this file to Git.
2. **Local Data**: All transaction data stays in `data/finance.db` on your machine.
3. **No Cloud Storage**: We don't use any cloud database or third-party analytics.
4. **Sanitization**: The `sanitize()` function is your privacy firewall.

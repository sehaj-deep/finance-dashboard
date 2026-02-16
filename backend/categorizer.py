import re
import os
import time
from groq import Groq
from database import get_db_session, CategoryRule
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def sanitize(text):
    """
    Strips Dates, Amounts, and Account Numbers from description.
    """
    # Remove Dates
    text = re.sub(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', '[DATE]', text)
    # Remove Amounts
    text = re.sub(r'\$?[\d,]+\.\d{2}', '[AMT]', text)
    # Remove Account Numbers (Sequence of 5+ digits)
    text = re.sub(r'\b\d{5,}\b', '[ACC#]', text)
    return text.strip()

def predict_category(description):
    """
    1. Check Local Rules.
    2. If no match -> Sanitize -> Call LLM (Groq Llama 3).
    """
    session = get_db_session()
    
    # 1. Check Rules (Naive keyword match)
    rules = session.query(CategoryRule).all()
    for rule in rules:
        if rule.keyword.lower() in description.lower():
            return rule.category
            
    # 2. Sanitize
    clean_desc = sanitize(description)
    
    # 3. Call LLM with Retry Logic
    # We ask for JSON to ensure strict output
    prompt = f"""Categorize this bank transaction description into ONE of these categories: Food, Transport, Utilities, Rent, Entertainment, Shopping, Income, Investment, Health, Other.

Transaction: "{clean_desc}"

Respond with valid JSON only in this format: {{"category": "CategoryName"}}. Do not add any other text."""

    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0, # Deterministic
                response_format={"type": "json_object"} # Force JSON mode
            )
            
            response_content = chat_completion.choices[0].message.content.strip()
            # Simple manual parsing or importing json
            import json
            data = json.loads(response_content)
            category = data.get("category", "Other")
            
            # Validation: Ensure it's in our allowed list (optional, but good safety)
            allowed = ["Food", "Transport", "Utilities", "Rent", "Entertainment", "Shopping", "Income", "Investment", "Health", "Other"]
            if category not in allowed:
                print(f"Invalid category '{category}' returned. Defaulting to Other.")
                category = "Other"
                
            print(f"Groq Prediction: '{clean_desc}' -> '{category}'")
            return category
            
        except Exception as e:
            if "429" in str(e):
                delay = base_delay * (2 ** attempt)
                print(f"Rate limited. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"Groq Error for '{clean_desc}': {e}")
                return "Other"
                
    print("Max retries exceeded.")
    return "Other"

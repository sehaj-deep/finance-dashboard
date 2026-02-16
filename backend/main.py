from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import shutil
import os
import ingest
import categorizer
from database import init_db, get_db_session, Transaction, Category, CategoryRule

app = FastAPI()

# Initialize DB
init_db()

class TransactionModel(BaseModel):
    id: int
    date: str
    description: str
    amount: float
    category: str

@app.get("/")
def read_root():
    return {"message": "Finance Dashboard API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"../data/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # Process file
    if file.filename.endswith('.pdf'):
        transactions = ingest.parse_pdf(file_location)
    elif file.filename.endswith('.csv'):
        transactions = ingest.parse_csv(file_location)
    else:
        raise HTTPException(400, "Invalid file format")
    
    # Save and Categorize
    session = get_db_session()
    saved_count = 0
    for txn in transactions:
        # Check duplicate? (Simple check by date+desc+amount for now)
        existing = session.query(Transaction).filter_by(
            date=txn['date'], description=txn['description'], amount=txn['amount']
        ).first()
        
        if not existing:
            # Predict Category
            cat = categorizer.predict_category(txn['description'])
            
            new_txn = Transaction(
                date=txn['date'],
                description=txn['description'],
                amount=txn['amount'],
                category=cat
            )
            session.add(new_txn)
            saved_count += 1
    
    session.commit()
    return {"filename": file.filename, "transactions_processed": len(transactions), "new_saved": saved_count}

@app.get("/transactions", response_model=List[TransactionModel])
def get_transactions():
    session = get_db_session()
    txns = session.query(Transaction).all()
    return [
        TransactionModel(
            id=t.id, date=t.date, description=t.description, 
            amount=t.amount, category=t.category
        ) for t in txns
    ]

@app.get("/summary")
def get_summary():
    session = get_db_session()
    # TODO: Calculate summary stats
    return {"status": "Not implemented yet"}

@app.get("/categories")
def get_categories():
    session = get_db_session()
    categories = session.query(Category).all()
    return [c.name for c in categories]
class TransactionUpdate(BaseModel):
    category: str

@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, txn_update: TransactionUpdate):
    session = get_db_session()
    txn = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(404, "Transaction not found")
    
    # 1. Update the transaction
    txn.category = txn_update.category
    
    # 2. Learn! Create a rule for future
    # We use the description as the keyword. 
    # To be safe, we might want to sanitize it or just use the whole thing.
    # Let's use the whole description for exact matching, or maybe a smart substring?
    # For now: EXACT MATCH of the description becomes a rule.
    keyword = txn.description.strip()
    
    existing_rule = session.query(CategoryRule).filter(CategoryRule.keyword == keyword).first()
    if existing_rule:
        existing_rule.category = txn_update.category
    else:
        new_rule = CategoryRule(keyword=keyword, category=txn_update.category)
        session.add(new_rule)
        
    session.commit()
    return {"status": "updated", "id": txn.id, "new_category": txn.category}

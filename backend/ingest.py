import pdfplumber
import pandas as pd
import re

def parse_pdf(file_path):
    transactions = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            for line in lines:
                # Look for lines that match credit card transaction format:
                # Jul 04 Jul 07 MARCH� NEWON MONTREAL QC Retail and Grocery 28.95
                # Pattern: Month Day Month Day Description Category Amount
                
                # Match lines with month abbreviation at start and amount at end
                match = re.match(
                    r'([A-Z][a-z]{2})\s+(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{1,2})\s+(.+?)\s+([\d,]+\.\d{2})$',
                    line
                )
                
                if match:
                    trans_month, trans_day, post_month, post_day, description_and_category, amount_str = match.groups()
                    
                    # 1. Immediate Payment Filter (Check raw text)
                    if "PAYMENT" in description_and_category.upper() or "PAIEMENT" in description_and_category.upper():
                        continue
                    
                    # Use the transaction date (first date)
                    date_str = f"{trans_month} {trans_day}"
                    
                    # Clean up description (remove category if present)
                    desc_parts = description_and_category.rsplit(' ', 3)  # Split from right to get category
                    if len(desc_parts) > 1:
                        # Last parts might be category, keep the merchant name
                        description = ' '.join(desc_parts[:-3]) if len(desc_parts) > 3 else desc_parts[0]
                    else:
                        description = description_and_category
                    
                    description = description.strip()
                    
                    # Skip payments/transfers
                    if "PAYMENT THANK YOU" in description.upper() or "PAIEMENT MERCI" in description.upper():
                        continue

                    try:
                        amount = float(amount_str.replace(',', ''))
                        
                        # Skip if description is too short or looks like a header
                        if len(description) > 3 and 'date' not in description.lower():
                            transactions.append({
                                "date": date_str,
                                "description": description,
                                "amount": amount
                            })
                    except:
                        continue
    
    return transactions

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    transactions = []
    
    # Normalize column names (case-insensitive)
    df.columns = df.columns.str.lower().str.strip()
    
    # Try to find the right columns
    date_col = None
    desc_col = None
    amount_col = None
    
    for col in df.columns:
        if 'date' in col:
            date_col = col
        elif 'desc' in col or 'merchant' in col or 'name' in col:
            desc_col = col
        elif 'amount' in col or 'total' in col or 'debit' in col or 'credit' in col:
            amount_col = col
    
    if not all([date_col, desc_col, amount_col]):
        # Fallback: assume first 3 columns are date, description, amount
        if len(df.columns) >= 3:
            date_col, desc_col, amount_col = df.columns[0], df.columns[1], df.columns[2]
        else:
            return []
    
    for _, row in df.iterrows():
        try:
            transactions.append({
                "date": str(row[date_col]),
                "description": str(row[desc_col]),
                "amount": float(row[amount_col])
            })
        except:
            continue
    
    return transactions

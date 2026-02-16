import sys
sys.path.append('.')
from ingest import parse_pdf
try:
    txns = parse_pdf('../data/eStatement.pdf')
    print("--- Transactions Found ---")
    for t in txns:
        print(f"DESC: '{t['description']}' | AMT: {t['amount']}")
except Exception as e:
    print(e)

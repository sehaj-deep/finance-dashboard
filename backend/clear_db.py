from database import get_db_session, Transaction
from sqlalchemy import text

def clear_transactions():
    session = get_db_session()
    try:
        # Delete all transactions
        session.query(Transaction).delete()
        session.commit()
        print("All transactions cleared successfully!")
    except Exception as e:
        print(f"Error clearing transactions: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    clear_transactions()

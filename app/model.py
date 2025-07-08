import psycopg2
from sentence_transformers import SentenceTransformer
import pandas as pd
from psycopg2.extras import execute_batch

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# DB Connection
def connect_db():
    return psycopg2.connect(
        host='aws-0-ap-south-1.pooler.supabase.com',
        port=6543,
        dbname='postgres',
        user='postgres.yajdnfumszppzcllnfrw',
        password='mWGGeZ4OHo1JGvFe'
    )
# Main function to insert embeddings
def insert_embeddings():
    conn = connect_db()
    cur = conn.cursor()

    # 1. Fetch records with NULL embeddings and non-empty text
    cur.execute("""
        SELECT book_id, text 
        FROM book_database 
        WHERE embedding IS NULL AND text IS NOT NULL
    """)
    rows = cur.fetchall()

    data = []
    for row in rows:
        book_id, text = row
        if text.strip():  # Skip if empty or whitespace
            embedding = model.encode(text).tolist()
            embedding_str = f"[{', '.join(map(str, embedding))}]"
            data.append((embedding_str, book_id))

    if data:
        update_query = """
            UPDATE book_database
            SET embedding = %s::vector
            WHERE book_id = %s
        """
        execute_batch(cur, update_query, data)
        conn.commit()
        print(f"✅ {len(data)} rows updated with embeddings.")
    else:
        print("⚠️ No eligible rows to update.")

    cur.close()
    conn.close()

# Run the script
insert_embeddings()








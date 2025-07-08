import psycopg2
from sentence_transformers import SentenceTransformer
from psycopg2.extras import execute_batch

# Use the same model from model.py
model = SentenceTransformer('all-MiniLM-L6-v2')
print(model.get_sentence_embedding_dimension())

# Connect to Supabase
def connect_db():
    return psycopg2.connect(
        host='aws-0-ap-south-1.pooler.supabase.com',
        port=6543,
        dbname='postgres',
        user='postgres.yajdnfumszppzcllnfrw',
        password='mWGGeZ4OHo1JGvFe'
    )
    
# Main function to get k similar books 
def get_top_k_similar_books(query: str, top_k: int = 1, expected_titles: list = None):
    query_embedding = model.encode(query).tolist()  # This is a Python list
    embedding_str = f"[{', '.join(map(str, query_embedding))}]"
    
    #step 2 : connect to database
    conn = connect_db()
    print('successfully connected to database')
    cur = conn.cursor()

    cur.execute("""
    SELECT title, authors, average_rating, text,1 - (embedding <=> %s::vector) AS similarity
    FROM book_database
    WHERE embedding is NOT NULL
    ORDER BY embedding <=> %s::vector
    LIMIT %s

    """, (embedding_str, embedding_str, top_k))


    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    for row in rows:
        print("Row fetched from database",row)
        results.append({
            "title": row[0],
            "authors": row[1],
            "average_rating": float(row[2]) if row[2] is not None else None,
            "text":row[3],
            "similarity": round(row[4], 4) if row[4] is not None else None
        })
    print('results')    
    # Optional: Compute precision@k
    # precision = None
    # if expected_titles:
    #     predicted_titles = [book["title"] for book in results]
    #     hits = sum(1 for t in expected_titles if t in predicted_titles)
    #     precision = round(hits / top_k, 2)

    return {"results": results}

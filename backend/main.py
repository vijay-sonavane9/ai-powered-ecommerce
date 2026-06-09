import sqlite3
import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Load keys
load_dotenv()

# 2. Initialize FastAPI
app = FastAPI()

# --- THE DIGITAL BOUNCER (CORS) ---
# This tells the backend to accept requests from your frontend website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------

embeddings_engine = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
chroma_client = chromadb.PersistentClient(path="./chroma_data")
chroma_collection = chroma_client.get_or_create_collection(name="product_embeddings")

@app.get("/")
def home():
    return {"status": "Online", "mode": "AI Semantic Search Ready"}

@app.get("/search")
def search_products(query: str):
    query_vector = embeddings_engine.embed_query(query)
    
    results = chroma_collection.query(
        query_embeddings=[query_vector],
        n_results=2
    )
    
    matched_ids = results['ids'][0]
    
    if not matched_ids:
        return {"results": []}
        
    sql_conn = sqlite3.connect('ecommerce.db')
    sql_cursor = sql_conn.cursor()
    
    format_places = ",".join(["?"] * len(matched_ids))
    sql_cursor.execute(f"SELECT id, name, description, price, image_url FROM products WHERE id IN ({format_places})", matched_ids)
    
    db_products = sql_cursor.fetchall()
    sql_conn.close()
    
    final_output = []
    for row in db_products:
        final_output.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "image_url": row[4]
        })
        
    return {"query": query, "results": final_output}
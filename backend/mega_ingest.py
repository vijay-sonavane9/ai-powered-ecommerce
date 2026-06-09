import sqlite3
import chromadb
import requests
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
embeddings_engine = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def load_massive_data():
    print("1. Fetching products from the internet...")
    # This pulls 20 realistic products from a free dummy-data API
    response = requests.get('https://fakestoreapi.com/products')
    api_products = response.json()
    
    print("2. Connecting to our databases...")
    sql_conn = sqlite3.connect('ecommerce.db')
    sql_cursor = sql_conn.cursor()
    
    chroma_client = chromadb.PersistentClient(path="./chroma_data")
    chroma_collection = chroma_client.get_or_create_collection(name="product_embeddings")

    print("\nStarting Mega-Injection Pipeline (This will take a minute or two)...\n")
    
    for product in api_products:
        # Check if we already have it
        sql_cursor.execute("SELECT id FROM products WHERE name = ?", (product["title"],))
        if sql_cursor.fetchone():
            print(f"Skipping: {product['title'][:30]}... (Already exists)")
            continue
            
        print(f"Processing: {product['title'][:40]}...")
        
        # A. Save to standard database
        sql_cursor.execute("""
            INSERT INTO products (name, description, price, image_url)
            VALUES (?, ?, ?, ?)
        """, (product["title"], product["description"], product["price"], product["image"]))
        
        product_id = str(sql_cursor.lastrowid)
        
        # B. AI Vector Generation
        text_to_analyze = f"{product['title']}: {product['description']}"
        vector_embedding = embeddings_engine.embed_query(text_to_analyze)
        
        # C. Save to AI Brain
        chroma_collection.add(
            ids=[product_id],
            embeddings=[vector_embedding],
            metadatas=[{"name": product["title"]}]
        )

    sql_conn.commit()
    sql_conn.close()
    print("\nMEGA-INGEST COMPLETE! You now have a full store inventory.")

if __name__ == "__main__":
    load_massive_data()
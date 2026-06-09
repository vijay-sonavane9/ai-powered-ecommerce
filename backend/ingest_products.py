import os
import sqlite3
import chromadb
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Unlock our vault of keys
load_dotenv()

# 2. Set up the Gemini Embeddings engine
# This is the tool that translates human words into AI vectors
embeddings_engine = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 3. Create mock products to put in our store
MOCK_PRODUCTS = [
    {
        "name": "CyberClick Mechanical Keyboard",
        "description": "A clicky, backlit mechanical keyboard designed for high-speed typing and gaming. Comes with customizable RGB lights and tactile switches.",
        "price": 89.99,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3"
    },
    {
        "name": "ErgoFlex Office Chair",
        "description": "Premium ergonomic mesh chair designed to support lower back and posture during long work hours. Adjustable armrests and breathable lumbar support.",
        "price": 249.50,
        "image_url": "https://images.unsplash.com/photo-1505797149-43b0069ec26b"
    },
    {
        "name": "ZenSound Wireless Headphones",
        "description": "Over-ear active noise-canceling headphones. Perfect for studying or working in noisy environments, featuring high-fidelity sound and a 40-hour battery life.",
        "price": 120.00,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
    }
]

def load_data():
    print("Connecting to standard database and AI brain...")
    # Connect to SQLite
    sql_conn = sqlite3.connect('ecommerce.db')
    sql_cursor = sql_conn.cursor()
    
    # Connect to ChromaDB (our vector storage folder)
    chroma_client = chromadb.PersistentClient(path="./chroma_data")
    # Create or grab an AI collection specifically for our products
    chroma_collection = chroma_client.get_or_create_collection(name="product_embeddings")

    print("\nStarting product injection pipeline...")
    
    for product in MOCK_PRODUCTS:
        # Check if the product already exists so we don't duplicate it
        sql_cursor.execute("SELECT id FROM products WHERE name = ?", (product["name"],))
        exists = sql_cursor.fetchone()
        
        if exists:
            print(f"-> '{product['name']}' already exists. Skipping.")
            continue
            
        print(f"-> Processing: {product['name']}")
        
        # A. Save to the standard SQLite filing cabinet
        sql_cursor.execute("""
            INSERT INTO products (name, description, price, image_url)
            VALUES (?, ?, ?, ?)
        """, (product["name"], product["description"], product["price"], product["image_url"]))
        
        # Get the unique ID that SQLite automatically assigned to this product
        product_id = str(sql_cursor.lastrowid)
        
        # B. Generate the AI Embedding using Gemini
        # We combine the title and description so the AI understands the full context
        text_to_analyze = f"{product['name']}: {product['description']}"
        vector_embedding = embeddings_engine.embed_query(text_to_analyze)
        
        # C. Save the vector into ChromaDB, linking it to the exact same product ID
        chroma_collection.add(
            ids=[product_id],
            embeddings=[vector_embedding],
            metadatas=[{"name": product["name"]}]
        )
        print(f"   Successfully saved product data and vector embedding!")

    # Finalize changes
    sql_conn.commit()
    sql_conn.close()
    print("\nAll done! Databases are loaded and ready.")

if __name__ == "__main__":
    load_data()
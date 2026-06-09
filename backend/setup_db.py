import sqlite3

def setup_database():
    print("Connecting to SQLite...")
    
    # This automatically creates a file named 'ecommerce.db' in your folder. No passwords needed!
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("Building the filing cabinets (Tables)...")
    
    # Cabinet 1: Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    );
    """)
    
    # Cabinet 2: Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL,
        image_url TEXT
    );
    """)
    
    # Save the changes and close
    conn.commit()
    conn.close()
    
    print("Success! Your SQLite database is fully built.")

if __name__ == "__main__":
    setup_database()
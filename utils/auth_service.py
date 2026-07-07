import sqlite3
import hashlib
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "hireready.db")

def db_init():
    """Initialize SQLite database for user accounts authentication."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    """Secure password hashing using SHA256 with a salt."""
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return hashed, salt

def register_user(name, email, password):
    """Register a new candidate. Returns (success, message)."""
    db_init()
    email_clean = email.strip().lower()
    
    if not name.strip() or not email_clean or not password:
        return False, "All fields are required."
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email_clean,))
        if cursor.fetchone():
            conn.close()
            return False, "An account with this email already exists."
            
        # Hash password and insert
        hashed, salt = hash_password(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, salt) VALUES (?, ?, ?, ?)",
            (name.strip(), email_clean, hashed, salt)
        )
        conn.commit()
        conn.close()
        return True, "Account registered successfully! Please log in."
    except Exception as e:
        conn.close()
        return False, f"Database error: {str(e)}"

def login_user(email, password):
    """Authenticate a candidate. Returns user dictionary if successful, else None."""
    db_init()
    email_clean = email.strip().lower()
    
    if not email_clean or not password:
        return None
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, email, password_hash, salt FROM users WHERE email = ?", (email_clean,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user_id, name, email_val, pwd_hash, salt = row
            check_hash, _ = hash_password(password, salt)
            if check_hash == pwd_hash:
                return {
                    "id": user_id,
                    "name": name,
                    "email": email_val
                }
        return None
    except Exception:
        if conn:
            conn.close()
        return None

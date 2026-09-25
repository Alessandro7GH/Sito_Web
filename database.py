import sqlite3
import os

DB_NAME = "something_bank.db"

def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    
    # Tabella Utenti
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            cash REAL NOT NULL DEFAULT 1000.0,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabella Transazioni
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Tabella Storico Azioni
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabella Inventario
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Tabella Obiettivi / Achievements
    cur.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            achieved INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Controllo di sicurezza per aggiungere la colonna 'ts' alla tabella inventory se manca
    try:
        cur.execute("SELECT ts FROM inventory LIMIT 1")
    except sqlite3.OperationalError:
        cur.execute("ALTER TABLE inventory ADD COLUMN ts TIMESTAMP")

    # Controllo di sicurezza per la colonna 'ts' se la tabella stock_history esisteva già senza di essa
    try:
        cur.execute("SELECT ts FROM stock_history LIMIT 1")
    except sqlite3.OperationalError:
        cur.execute("ALTER TABLE stock_history ADD COLUMN ts TIMESTAMP")

    conn.commit()
    conn.close()

def create_or_get_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if row:
        uid = row["id"]
    else:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, ""))
        conn.commit()
        uid = cur.lastrowid
    conn.close()
    return uid

def get_user(conn, uid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (uid,))
    return cur.fetchone()

if __name__ == "__main__":
    init_db()
    print("Database inizializzato con successo.")
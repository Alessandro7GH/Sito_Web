"""
Gestione database SQLite per SOMETHING BANK.

Crea automaticamente il database e tutte le tabelle al primo avvio.
"""

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
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Tabella Inventario Oggetti
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            buy_price REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Tabella Investimenti / Azioni Possedute
    cur.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stock_symbol TEXT NOT NULL,
            shares REAL NOT NULL DEFAULT 0,
            avg_buy_price REAL NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Tabella Mercato Azionario (con Prezzo Base del Giorno)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS market (
            symbol TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            current_price REAL NOT NULL,
            base_price REAL NOT NULL DEFAULT 0.0,
            last_reset_date TEXT
        )
    """)

    # Tabella Storico Prezzi per il Grafico
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(symbol) REFERENCES market(symbol)
        )
    """)

    # Tabella Aziende Possedute dagli Utenti
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies_owned (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            hourly_revenue REAL DEFAULT 10.0,
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

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database inizializzato con successo.")
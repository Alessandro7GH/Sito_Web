"""Gestione database SQLite per SOMETHING BANK.

Crea automaticamente il database e tutte le tabelle al primo avvio.
Nessun servizio esterno: tutto in locale in un singolo file .db.

Tabelle:
  users, transactions, inventory, investments, market, companies_owned, achievements
"""

import os
import sqlite3
import time
import uuid

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "something_bank.db")

START_CASH = 100000.0


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            cash REAL NOT NULL,
            created_at REAL NOT NULL,
            last_interest REAL NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            ts REAL NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            ts REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS investments (
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            shares INTEGER NOT NULL DEFAULT 0,
            last_buy_ts REAL NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, company_id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS market (
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            price REAL NOT NULL,
            change_pct REAL NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, company_id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS companies_owned (
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            bought_at REAL NOT NULL,
            PRIMARY KEY (user_id, company_id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS achievements (
            user_id TEXT NOT NULL,
            code TEXT NOT NULL,
            unlocked_at REAL NOT NULL,
            PRIMARY KEY (user_id, code),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )
    conn.commit()
    conn.close()


def create_user(name):
    from data.companies import COMPANIES

    uid = str(uuid.uuid4())
    now = time.time()
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (id, name, cash, created_at, last_interest) VALUES (?,?,?,?,?)",
        (uid, name, START_CASH, now, now),
    )
    c.execute(
        "INSERT INTO transactions (user_id, ts, description, amount) VALUES (?,?,?,?)",
        (uid, now, "Bonus iniziale", START_CASH),
    )
    for comp in COMPANIES:
        c.execute(
            "INSERT INTO market (user_id, company_id, price, change_pct) VALUES (?,?,?,?)",
            (uid, comp["id"], comp["price"], 0.0),
        )
    conn.commit()
    conn.close()
    return uid


def get_user(conn, uid):
    return conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
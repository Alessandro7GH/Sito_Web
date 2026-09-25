import random
import time

from flask import Flask, jsonify, render_template, request
import database
from data.companies import COMPANIES, COMPANIES_BY_ID
from data.products import (
    CATEGORIES,
    CATEGORY_LABELS,
    PRODUCTS,
    PRODUCTS_BY_ID,
    PROPERTY_CATEGORIES,
    USELESS_CATEGORIES,
)

app = Flask(__name__)

HISTORY_POINTS = 180   # punti storici inviati per azienda
HISTORY_KEEP = 800     # punti conservati nel DB per azienda

"""Gestione database SQLite per SOMETHING BANK.

Tabelle: users, transactions, inventory, investments, market,
         companies_owned, achievements, price_history
"""

import os
import random
import sqlite3
import time
import uuid

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "something_bank.db")

START_CASH = 100000.0


def today_str():
    """Data locale corrente 'YYYY-MM-DD' (per il reset della mezzanotte)."""
    return time.strftime("%Y-%m-%d", time.localtime())


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _safe_alter(conn, sql):
    try:
        conn.execute(sql)
    except sqlite3.OperationalError:
        pass  # colonna già esistente


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
            amount REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            ts REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS investments (
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            shares INTEGER NOT NULL DEFAULT 0,
            last_buy_ts REAL NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, company_id)
        );

        CREATE TABLE IF NOT EXISTS market (
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            price REAL NOT NULL,
            change_pct REAL NOT NULL DEFAULT 0,
            ref_price REAL NOT NULL DEFAULT 0,
            ref_day TEXT NOT NULL DEFAULT '',
            PRIMARY KEY (user_id, company_id)
        );

        CREATE TABLE IF NOT EXISTS companies_owned (
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            bought_at REAL NOT NULL,
            PRIMARY KEY (user_id, company_id)
        );

        CREATE TABLE IF NOT EXISTS achievements (
            user_id TEXT NOT NULL,
            code TEXT NOT NULL,
            unlocked_at REAL NOT NULL,
            PRIMARY KEY (user_id, code)
        );

        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            company_id TEXT NOT NULL,
            ts REAL NOT NULL,
            price REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_hist ON price_history(user_id, company_id, ts);
        """
    )
    # Migrazioni leggere per DB creati con versioni precedenti
    _safe_alter(conn, "ALTER TABLE market ADD COLUMN ref_price REAL NOT NULL DEFAULT 0")
    _safe_alter(conn, "ALTER TABLE market ADD COLUMN ref_day TEXT NOT NULL DEFAULT ''")
    conn.commit()
    conn.close()


def create_user(name):
    from data.companies import COMPANIES

    uid = str(uuid.uuid4())
    now = time.time()
    day = today_str()
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
        base = comp["price"]
        c.execute(
            "INSERT INTO market (user_id, company_id, price, change_pct, ref_price, ref_day) VALUES (?,?,?,?,?,?)",
            (uid, comp["id"], base, 0.0, base, day),
        )
        # Semina una storia iniziale (~48 punti nelle ultime ~8 ore) attorno al prezzo base
        points = 48
        span = 8 * 3600
        price = base
        for i in range(points):
            t = now - span + (span / points) * i
            price = max(0.5, price * (1 + random.gauss(0, comp["volatility"])))
            c.execute(
                "INSERT INTO price_history (user_id, company_id, ts, price) VALUES (?,?,?,?)",
                (uid, comp["id"], t, price),
            )
        c.execute("UPDATE market SET price=? WHERE user_id=? AND company_id=?", (price, uid, comp["id"]))
    conn.commit()
    conn.close()
    return uid


def get_user(conn, uid):
    return conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()



def pick_lang(value):
    return "en" if str(value).lower() == "en" else "it"


ACHIEVEMENTS = [
    {"code": "POVERO", "it": "POVERO", "en": "BROKE", "desc_it": "Spendi tutti i tuoi soldi.", "desc_en": "Spend all your money.", "hidden": False},
    {"code": "RICCO", "it": "RICCO", "en": "RICH", "desc_it": "Supera €1.000.000.", "desc_en": "Go past €1,000,000.", "hidden": False},
    {"code": "MILIONARIO", "it": "MILIONARIO", "en": "MILLIONAIRE", "desc_it": "Supera €10.000.000.", "desc_en": "Go past €10,000,000.", "hidden": False},
    {"code": "PERCHE", "it": "PERCHÉ?", "en": "WHY?", "desc_it": "Compra 100 oggetti inutili.", "desc_en": "Buy 100 useless things.", "hidden": True},
    {"code": "COLLEZIONISTA", "it": "COLLEZIONISTA", "en": "COLLECTOR", "desc_it": "Compra 50 oggetti diversi.", "desc_en": "Buy 50 different items.", "hidden": False},
    {"code": "INVESTITORE", "it": "INVESTITORE", "en": "INVESTOR", "desc_it": "Compra la prima azione.", "desc_en": "Buy your first share.", "hidden": False},
    {"code": "CAPITALISTA", "it": "CAPITALISTA", "en": "CAPITALIST", "desc_it": "Possiedi il 10% di un'azienda.", "desc_en": "Own 10% of a company.", "hidden": True},
    {"code": "MONOPOLIO", "it": "MONOPOLIO", "en": "MONOPOLY", "desc_it": "Compra un'intera azienda.", "desc_en": "Buy an entire company.", "hidden": False},
    {"code": "CAMBIATO_IDEA", "it": "HO CAMBIATO IDEA", "en": "CHANGED MY MIND", "desc_it": "Vendi qualcosa entro 10 secondi dall'acquisto.", "desc_en": "Sell something within 10 seconds of buying.", "hidden": True},
    {"code": "INUTILE", "it": "ASSOLUTAMENTE INUTILE", "en": "ABSOLUTELY USELESS", "desc_it": "Spendi €10.000 in oggetti inutili.", "desc_en": "Spend €10,000 on useless things.", "hidden": True},
]
ACHIEVEMENTS_BY_CODE = {a["code"]: a for a in ACHIEVEMENTS}

BUY_PHRASES = [
    {"it": "Acquistato.", "en": "Purchased."},
    {"it": "Complimenti.", "en": "Congratulations."},
    {"it": "Scelta discutibile.", "en": "Questionable choice."},
    {"it": "{name}, sei sicuro?", "en": "{name}, are you sure?"},
    {"it": "Tecnicamente ne avevi bisogno.", "en": "Technically you needed it."},
    {"it": "Nessuno sa perché tu l'abbia comprato.", "en": "Nobody knows why you bought it."},
    {"it": "{name}, questa è probabilmente una pessima idea.", "en": "{name}, this is probably a terrible idea."},
    {"it": "Fatto. Non torniamo indietro.", "en": "Done. No going back."},
    {"it": "Il patrimonio di {name} ringrazia. Forse.", "en": "{name}'s net worth thanks you. Maybe."},
]

PLAYER_EVENTS = [
    {"it": "Hai trovato €20.", "en": "You found €20.", "amount": 20},
    {"it": "Hai ricevuto un regalo.", "en": "You received a gift.", "amount": 300},
    {"it": "Hai perso il portafoglio.", "en": "You lost your wallet.", "amount": -200},
    {"it": "Hai comprato qualcosa mentre dormivi.", "en": "You bought something while sleeping.", "amount": -79},
    {"it": "Una persona a caso ti deve €50.", "en": "A random person owes you €50.", "amount": 50},
    {"it": "{name}, hai vinto una lotteria a cui non avevi partecipato.", "en": "{name}, you won a lottery you didn't enter.", "amount": 1200},
    {"it": "Multa per parcheggio immaginario.", "en": "Fine for imaginary parking.", "amount": -140},
    {"it": "La tua azienda sta andando molto bene.", "en": "Your company is doing very well.", "amount": 8420, "needs_company": True},
]

INTEREST_TXT = {"it": "Gli interessi hanno deciso di esistere.", "en": "Interest has decided to exist."}


def add_transaction(conn, uid, description, amount):
    conn.execute(
        "INSERT INTO transactions (user_id, ts, description, amount) VALUES (?,?,?,?)",
        (uid, time.time(), description, amount),
    )


def unlock(conn, uid, code, lang):
    exists = conn.execute("SELECT 1 FROM achievements WHERE user_id=? AND code=?", (uid, code)).fetchone()
    if exists:
        return None
    conn.execute("INSERT INTO achievements (user_id, code, unlocked_at) VALUES (?,?,?)", (uid, code, time.time()))
    a = ACHIEVEMENTS_BY_CODE[code]
    return {"code": code, "name": a[lang], "desc": a["desc_" + lang]}


def compute_state(conn, uid, lang="it", with_history=True):
    user = database.get_user(conn, uid)
    if not user:
        return None
    cash = user["cash"]

    inv_rows = conn.execute("SELECT * FROM inventory WHERE user_id=? ORDER BY ts DESC", (uid,)).fetchall()
    property_value = 0.0
    objects_value = 0.0
    inventory = []
    for r in inv_rows:
        if r["category"] in PROPERTY_CATEGORIES:
            property_value += r["price"]
        else:
            objects_value += r["price"]
        inventory.append({"product_id": r["product_id"], "name": r["name"], "price": r["price"], "category": r["category"]})

    owned_ids = {r["company_id"] for r in conn.execute("SELECT company_id FROM companies_owned WHERE user_id=?", (uid,)).fetchall()}
    market_rows = conn.execute("SELECT * FROM market WHERE user_id=?", (uid,)).fetchall()
    price_map = {r["company_id"]: r["price"] for r in market_rows}
    change_map = {r["company_id"]: r["change_pct"] for r in market_rows}
    ref_map = {r["company_id"]: r["ref_price"] for r in market_rows}
    inv_shares = {r["company_id"]: r["shares"] for r in conn.execute("SELECT * FROM investments WHERE user_id=?", (uid,)).fetchall()}

    hist_map = {}
    if with_history:
        for comp in COMPANIES:
            rows = conn.execute(
                "SELECT ts, price FROM price_history WHERE user_id=? AND company_id=? ORDER BY ts DESC LIMIT ?",
                (uid, comp["id"], HISTORY_POINTS),
            ).fetchall()
            hist_map[comp["id"]] = [{"t": round(r["ts"], 1), "p": round(r["price"], 4)} for r in reversed(rows)]

    stocks_value = 0.0
    companies_value = 0.0
    market = []
    for comp in COMPANIES:
        cid = comp["id"]
        price = price_map.get(cid, comp["price"])
        shares = inv_shares.get(cid, 0)
        owned = cid in owned_ids
        market_cap = price * comp["shares_outstanding"]
        ref = ref_map.get(cid, price) or price
        if owned:
            companies_value += market_cap
        else:
            stocks_value += shares * price
        day_change = (price / ref - 1) * 100 if ref else 0
        market.append({
            "id": cid, "name": comp["name"], "price": round(price, 2),
            "change": round(change_map.get(cid, 0.0), 2), "ref": round(ref, 2),
            "day_change": round(day_change, 2), "shares": shares,
            "shares_outstanding": comp["shares_outstanding"], "value": round(shares * price, 2),
            "market_cap": round(market_cap, 2), "owned": owned, "history": hist_map.get(cid, []),
        })

    net_worth = cash + stocks_value + companies_value + property_value + objects_value

    tx_rows = conn.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY ts DESC LIMIT 100", (uid,)).fetchall()
    history = [{"description": r["description"], "amount": r["amount"], "ts": r["ts"]} for r in tx_rows]

    unlocked = {r["code"] for r in conn.execute("SELECT code FROM achievements WHERE user_id=?", (uid,)).fetchall()}
    ach_list = []
    for a in ACHIEVEMENTS:
        is_unlocked = a["code"] in unlocked
        shown = is_unlocked or not a["hidden"]
        ach_list.append({
            "code": a["code"],
            "name": a[lang] if shown else "???",
            "desc": a["desc_" + lang] if shown else ("Achievement segreto." if lang == "it" else "Secret achievement."),
            "hidden": a["hidden"], "unlocked": is_unlocked,
        })

    return {
        "id": uid, "name": user["name"], "cash": round(cash, 2), "net_worth": round(net_worth, 2),
        "breakdown": {
            "cash": round(max(cash, 0), 2), "stocks": round(stocks_value, 2),
            "companies": round(companies_value, 2), "property": round(property_value, 2),
            "objects": round(objects_value, 2), "debt": round(min(cash, 0), 2),
        },
        "inventory": inventory, "market": market, "history": history, "achievements": ach_list,
    }


def check_achievements(conn, uid, lang):
    new = []
    user = database.get_user(conn, uid)
    cash = user["cash"]
    state = compute_state(conn, uid, lang, with_history=False)
    net = state["net_worth"]

    if cash <= 0:
        a = unlock(conn, uid, "POVERO", lang)
        if a: new.append(a)
    if net >= 1_000_000:
        a = unlock(conn, uid, "RICCO", lang)
        if a: new.append(a)
    if net >= 10_000_000:
        a = unlock(conn, uid, "MILIONARIO", lang)
        if a: new.append(a)

    useless_rows = conn.execute("SELECT category, price FROM inventory WHERE user_id=?", (uid,)).fetchall()
    useless_count = sum(1 for r in useless_rows if r["category"] in USELESS_CATEGORIES)
    useless_spend = sum(r["price"] for r in useless_rows if r["category"] in USELESS_CATEGORIES)
    if useless_count >= 100:
        a = unlock(conn, uid, "PERCHE", lang)
        if a: new.append(a)
    if useless_spend >= 10000:
        a = unlock(conn, uid, "INUTILE", lang)
        if a: new.append(a)

    distinct = conn.execute("SELECT COUNT(DISTINCT product_id) AS n FROM inventory WHERE user_id=?", (uid,)).fetchone()["n"]
    if distinct >= 50:
        a = unlock(conn, uid, "COLLEZIONISTA", lang)
        if a: new.append(a)

    for inv in conn.execute("SELECT * FROM investments WHERE user_id=?", (uid,)).fetchall():
        comp = COMPANIES_BY_ID.get(inv["company_id"])
        if comp and inv["shares"] >= 0.10 * comp["shares_outstanding"]:
            a = unlock(conn, uid, "CAPITALISTA", lang)
            if a: new.append(a)
            break
    return new


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bank")
def bank():
    return render_template("bank.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/investments")
def investments():
    return render_template("investments.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(force=True) or {}
    lang = pick_lang(data.get("lang", "it"))
    name = (data.get("name") or "").strip()[:40]
    if not name:
        return jsonify({"error": "Serve un nome." if lang == "it" else "A name is required."}), 400
    uid = database.create_user(name)
    conn = database.get_conn()
    state = compute_state(conn, uid, lang)
    conn.close()
    return jsonify(state)


@app.route("/api/state")
def api_state():
    uid = request.args.get("pid", "")
    lang = pick_lang(request.args.get("lang", "it"))
    conn = database.get_conn()
    state = compute_state(conn, uid, lang)
    conn.close()
    if not state:
        return jsonify({"error": "not_found"}), 404
    return jsonify(state)


@app.route("/api/catalog")
def api_catalog():
    categories = [{"key": k, "label_it": v["it"], "label_en": v["en"]} for k, v in CATEGORY_LABELS.items()]
    products = [
        {
            "id": p["id"], "price": p["price"], "category": p["category"],
            "name": p["name"], "name_en": p["name_en"],
            "description": p["description"], "description_en": p["description_en"],
        }
        for p in PRODUCTS
    ]
    return jsonify({"categories": categories, "products": products})


@app.route("/api/buy", methods=["POST"])
def api_buy():
    data = request.get_json(force=True) or {}
    lang = pick_lang(data.get("lang", "it"))
    uid = data.get("pid", "")
    product_id = data.get("product_id", "")
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    product = PRODUCTS_BY_ID.get(product_id)
    if not user or not product:
        conn.close()
        return jsonify({"error": "not_found"}), 404

    cash = user["cash"]
    price = float(product["price"])
    pname = product["name_en"] if lang == "en" else product["name"]
    conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (price, uid))
    conn.execute(
        "INSERT INTO inventory (user_id, product_id, name, price, category, ts) VALUES (?,?,?,?,?,?)",
        (uid, product_id, pname, price, product["category"], time.time()),
    )
    add_transaction(conn, uid, pname, -price)

    went_into_debt = cash >= 0 and (cash - price) < 0
    new_ach = check_achievements(conn, uid, lang)
    conn.commit()
    phrase = random.choice(BUY_PHRASES)[lang].format(name=user["name"])
    state = compute_state(conn, uid, lang)
    conn.close()
    return jsonify({"ok": True, "phrase": phrase, "went_into_debt": went_into_debt, "new_achievements": new_ach, "state": state})


@app.route("/api/buy_stock", methods=["POST"])
def api_buy_stock():
    data = request.get_json(force=True) or {}
    lang = pick_lang(data.get("lang", "it"))
    uid = data.get("pid", "")
    cid = data.get("company_id", "")
    shares = max(1, int(data.get("shares", 1) or 1))
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    comp = COMPANIES_BY_ID.get(cid)
    if not user or not comp:
        conn.close()
        return jsonify({"error": "not_found"}), 404
    if conn.execute("SELECT 1 FROM companies_owned WHERE user_id=? AND company_id=?", (uid, cid)).fetchone():
        conn.close()
        return jsonify({"error": "Possiedi già l'intera azienda." if lang == "it" else "You already own the whole company."}), 400

    price = conn.execute("SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)).fetchone()["price"]
    cost = price * shares
    if user["cash"] < cost:
        conn.close()
        return jsonify({"ok": False, "error": "Non puoi permettertelo." if lang == "it" else "You can't afford it."}), 400

    conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cost, uid))
    existing = conn.execute("SELECT shares FROM investments WHERE user_id=? AND company_id=?", (uid, cid)).fetchone()
    first_stock = existing is None or existing["shares"] == 0
    if existing:
        conn.execute("UPDATE investments SET shares = shares + ?, last_buy_ts = ? WHERE user_id=? AND company_id=?", (shares, time.time(), uid, cid))
    else:
        conn.execute("INSERT INTO investments (user_id, company_id, shares, last_buy_ts) VALUES (?,?,?,?)", (uid, cid, shares, time.time()))
    label = f"{shares}x {comp['name']} " + ("(azioni)" if lang == "it" else "(shares)")
    add_transaction(conn, uid, label, -cost)

    new_ach = []
    if first_stock:
        a = unlock(conn, uid, "INVESTITORE", lang)
        if a: new_ach.append(a)
    new_ach += check_achievements(conn, uid, lang)
    conn.commit()
    state = compute_state(conn, uid, lang)
    conn.close()
    return jsonify({"ok": True, "new_achievements": new_ach, "state": state})


@app.route("/api/sell_stock", methods=["POST"])
def api_sell_stock():
    data = request.get_json(force=True) or {}
    lang = pick_lang(data.get("lang", "it"))
    uid = data.get("pid", "")
    cid = data.get("company_id", "")
    shares = max(1, int(data.get("shares", 1) or 1))
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    comp = COMPANIES_BY_ID.get(cid)
    inv = conn.execute("SELECT * FROM investments WHERE user_id=? AND company_id=?", (uid, cid)).fetchone()
    if not user or not comp or not inv or inv["shares"] < shares:
        conn.close()
        return jsonify({"error": "Non hai abbastanza azioni." if lang == "it" else "You don't have enough shares."}), 400

    price = conn.execute("SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)).fetchone()["price"]
    gain = price * shares
    conn.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (gain, uid))
    conn.execute("UPDATE investments SET shares = shares - ? WHERE user_id=? AND company_id=?", (shares, uid, cid))
    label = (f"Venduto {shares}x {comp['name']}" if lang == "it" else f"Sold {shares}x {comp['name']}")
    add_transaction(conn, uid, label, gain)

    new_ach = []
    if time.time() - inv["last_buy_ts"] <= 10:
        a = unlock(conn, uid, "CAMBIATO_IDEA", lang)
        if a: new_ach.append(a)
    new_ach += check_achievements(conn, uid, lang)
    conn.commit()
    state = compute_state(conn, uid, lang)
    conn.close()
    return jsonify({"ok": True, "new_achievements": new_ach, "state": state})


@app.route("/api/buy_company", methods=["POST"])
def api_buy_company():
    data = request.get_json(force=True) or {}
    lang = pick_lang(data.get("lang", "it"))
    uid = data.get("pid", "")
    cid = data.get("company_id", "")
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    comp = COMPANIES_BY_ID.get(cid)
    if not user or not comp:
        conn.close()
        return jsonify({"error": "not_found"}), 404
    if conn.execute("SELECT 1 FROM companies_owned WHERE user_id=? AND company_id=?", (uid, cid)).fetchone():
        conn.close()
        return jsonify({"error": "Già tua." if lang == "it" else "Already yours."}), 400

    price = conn.execute("SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)).fetchone()["price"]
    market_cap = price * comp["shares_outstanding"]
    if user["cash"] < market_cap:
        conn.close()
        return jsonify({"ok": False, "error": "Non puoi permettertelo." if lang == "it" else "You can't afford it."}), 400

    conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (market_cap, uid))
    conn.execute("INSERT INTO companies_owned (user_id, company_id, bought_at) VALUES (?,?,?)", (uid, cid, time.time()))
    label = (f"Acquisto azienda: {comp['name']}" if lang == "it" else f"Company purchase: {comp['name']}")
    add_transaction(conn, uid, label, -market_cap)
    new_ach = []
    a = unlock(conn, uid, "MONOPOLIO", lang)
    if a: new_ach.append(a)
    new_ach += check_achievements(conn, uid, lang)
    conn.commit()
    state = compute_state(conn, uid, lang)
    conn.close()
    return jsonify({"ok": True, "company_name": comp["name"], "new_achievements": new_ach, "state": state})


@app.route("/api/tick", methods=["POST"])
def api_tick():
    data = request.get_json(force=True) or {}
    lang = pick_lang(data.get("lang", "it"))
    uid = data.get("pid", "")
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    if not user:
        conn.close()
        return jsonify({"error": "not_found"}), 404

    events = []
    now = time.time()
    day = database.today_str()

    # 1) Random walk + registrazione storia + reset mezzanotte
    for comp in COMPANIES:
        cid = comp["id"]
        row = conn.execute("SELECT price, ref_day FROM market WHERE user_id=? AND company_id=?", (uid, cid)).fetchone()
        old = row["price"]
        drift = random.gauss(0, comp["volatility"])
        new = max(0.5, old * (1 + drift))
        change = (new / old - 1) * 100 if old else 0
        if row["ref_day"] != day:
            # nuova giornata: il riferimento (chiusura precedente) diventa il prezzo di apertura
            conn.execute("UPDATE market SET price=?, change_pct=?, ref_price=?, ref_day=? WHERE user_id=? AND company_id=?",
                         (new, change, new, day, uid, cid))
        else:
            conn.execute("UPDATE market SET price=?, change_pct=? WHERE user_id=? AND company_id=?",
                         (new, change, uid, cid))
        conn.execute("INSERT INTO price_history (user_id, company_id, ts, price) VALUES (?,?,?,?)", (uid, cid, now, new))

    # 2) Evento di mercato (raro)
    if random.random() < 0.22:
        comp = random.choice(COMPANIES)
        ev = random.choice(comp["events"])
        row = conn.execute("SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, comp["id"])).fetchone()
        old = row["price"]
        new = max(0.5, old * (1 + ev["pct"] / 100))
        change = (new / old - 1) * 100 if old else 0
        conn.execute("UPDATE market SET price=?, change_pct=? WHERE user_id=? AND company_id=?", (new, change, uid, comp["id"]))
        conn.execute("INSERT INTO price_history (user_id, company_id, ts, price) VALUES (?,?,?,?)", (uid, comp["id"], now + 0.001, new))
        events.append({"type": "market", "company": comp["name"], "text": ev[lang], "pct": ev["pct"]})

    # 3) Entrate dalle aziende possedute
    owned = conn.execute("SELECT company_id FROM companies_owned WHERE user_id=?", (uid,)).fetchall()
    for o in owned:
        comp = COMPANIES_BY_ID.get(o["company_id"])
        if comp and random.random() < 0.25:
            price = conn.execute("SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, comp["id"])).fetchone()["price"]
            income = round(price * comp["shares_outstanding"] * comp["income"], 2)
            if income > 0:
                conn.execute("UPDATE users SET cash = cash + ? WHERE id=?", (income, uid))
                lbl = (f"Entrate da {comp['name']}" if lang == "it" else f"Income from {comp['name']}")
                add_transaction(conn, uid, lbl, income)
                events.append({"type": "income", "text": lbl, "amount": income})

    # 4) Interessi sul debito
    user = database.get_user(conn, uid)
    if user["cash"] < 0 and random.random() < 0.5:
        interest = round(abs(user["cash"]) * 0.02, 2)
        if interest > 0:
            conn.execute("UPDATE users SET cash = cash - ? WHERE id=?", (interest, uid))
            add_transaction(conn, uid, INTEREST_TXT[lang], -interest)
            events.append({"type": "interest", "text": INTEREST_TXT[lang], "amount": -interest})

    # 5) Evento casuale del giocatore (raro)
    if random.random() < 0.15:
        has_company = len(owned) > 0
        pool = [e for e in PLAYER_EVENTS if not e.get("needs_company") or has_company]
        ev = random.choice(pool)
        amount = ev["amount"]
        conn.execute("UPDATE users SET cash = cash + ? WHERE id=?", (amount, uid))
        text = ev[lang].format(name=user["name"])
        add_transaction(conn, uid, text, amount)
        events.append({"type": "player", "text": text, "amount": amount})

    # 6) Pulizia storia (mantieni gli ultimi HISTORY_KEEP punti per azienda)
    if random.random() < 0.3:
        for comp in COMPANIES:
            conn.execute(
                "DELETE FROM price_history WHERE id IN ("
                "  SELECT id FROM price_history WHERE user_id=? AND company_id=? "
                "  ORDER BY ts DESC LIMIT -1 OFFSET ?)",
                (uid, comp["id"], HISTORY_KEEP),
            )

    new_ach = check_achievements(conn, uid, lang)
    conn.commit()
    state = compute_state(conn, uid, lang)
    conn.close()
    return jsonify({"ok": True, "events": events, "new_achievements": new_ach, "state": state})


if __name__ == "__main__":
    database.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
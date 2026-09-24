"""SOMETHING BANK — una web app ironica in stile Neal.fun.

Backend: Python + Flask + SQLite (tutto in locale).
Avvio:  python app.py   ->   http://127.0.0.1:5000
"""

import random
import time

from flask import Flask, jsonify, render_template, request

import database
from data.companies import COMPANIES, COMPANIES_BY_ID
from data.products import (
    CATEGORIES,
    PRODUCTS,
    PRODUCTS_BY_ID,
    PROPERTY_CATEGORIES,
    USELESS_CATEGORIES,
)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Achievement
# ---------------------------------------------------------------------------
ACHIEVEMENTS = [
    {"code": "POVERO", "name": "POVERO", "desc": "Spendi tutti i tuoi soldi.", "hidden": False},
    {"code": "RICCO", "name": "RICCO", "desc": "Supera €1.000.000.", "hidden": False},
    {"code": "MILIONARIO", "name": "MILIONARIO", "desc": "Supera €10.000.000.", "hidden": False},
    {"code": "PERCHE", "name": "PERCHÉ?", "desc": "Compra 100 oggetti inutili.", "hidden": True},
    {"code": "COLLEZIONISTA", "name": "COLLEZIONISTA", "desc": "Compra 50 oggetti diversi.", "hidden": False},
    {"code": "INVESTITORE", "name": "INVESTITORE", "desc": "Compra la prima azione.", "hidden": False},
    {"code": "CAPITALISTA", "name": "CAPITALISTA", "desc": "Possiedi il 10% di un'azienda.", "hidden": True},
    {"code": "MONOPOLIO", "name": "MONOPOLIO", "desc": "Compra un'intera azienda.", "hidden": False},
    {"code": "CAMBIATO_IDEA", "name": "HO CAMBIATO IDEA", "desc": "Vendi qualcosa entro 10 secondi dall'acquisto.", "hidden": True},
    {"code": "INUTILE", "name": "ASSOLUTAMENTE INUTILE", "desc": "Spendi €10.000 in oggetti inutili.", "hidden": True},
]
ACHIEVEMENTS_BY_CODE = {a["code"]: a for a in ACHIEVEMENTS}

# Frasi ironiche mostrate dopo un acquisto (usa {name})
BUY_PHRASES = [
    "Acquistato.",
    "Complimenti.",
    "Scelta discutibile.",
    "{name}, sei sicuro?",
    "Tecnicamente ne avevi bisogno.",
    "Nessuno sa perché tu l'abbia comprato.",
    "{name}, questa è probabilmente una pessima idea.",
    "Fatto. Non torniamo indietro.",
    "Il patrimonio di {name} ringrazia. Forse.",
]

# Eventi casuali del giocatore
PLAYER_EVENTS = [
    {"text": "Hai trovato €20.", "amount": 20},
    {"text": "Hai ricevuto un regalo.", "amount": 300},
    {"text": "Hai perso il portafoglio.", "amount": -200},
    {"text": "Hai comprato qualcosa mentre dormivi.", "amount": -79},
    {"text": "Una persona a caso ti deve €50.", "amount": 50},
    {"text": "{name}, hai vinto una lotteria a cui non avevi partecipato.", "amount": 1200},
    {"text": "Multa per parcheggio immaginario.", "amount": -140},
    {"text": "La tua azienda sta andando molto bene.", "amount": 8420, "needs_company": True},
]


# ---------------------------------------------------------------------------
# Helpers di stato
# ---------------------------------------------------------------------------
def add_transaction(conn, uid, description, amount):
    conn.execute(
        "INSERT INTO transactions (user_id, ts, description, amount) VALUES (?,?,?,?)",
        (uid, time.time(), description, amount),
    )


def unlock(conn, uid, code):
    """Sblocca un achievement se non già presente. Ritorna il dict se nuovo."""
    exists = conn.execute(
        "SELECT 1 FROM achievements WHERE user_id=? AND code=?", (uid, code)
    ).fetchone()
    if exists:
        return None
    conn.execute(
        "INSERT INTO achievements (user_id, code, unlocked_at) VALUES (?,?,?)",
        (uid, code, time.time()),
    )
    return ACHIEVEMENTS_BY_CODE[code]


def compute_state(conn, uid):
    user = database.get_user(conn, uid)
    if not user:
        return None
    cash = user["cash"]

    # Inventario
    inv_rows = conn.execute(
        "SELECT * FROM inventory WHERE user_id=? ORDER BY ts DESC", (uid,)
    ).fetchall()
    property_value = 0.0
    objects_value = 0.0
    inventory = []
    for r in inv_rows:
        if r["category"] in PROPERTY_CATEGORIES:
            property_value += r["price"]
        else:
            objects_value += r["price"]
        inventory.append(
            {"product_id": r["product_id"], "name": r["name"], "price": r["price"], "category": r["category"]}
        )

    # Aziende possedute
    owned_rows = conn.execute(
        "SELECT company_id FROM companies_owned WHERE user_id=?", (uid,)
    ).fetchall()
    owned_ids = {r["company_id"] for r in owned_rows}

    # Mercato + partecipazioni
    market_rows = conn.execute("SELECT * FROM market WHERE user_id=?", (uid,)).fetchall()
    price_map = {r["company_id"]: r["price"] for r in market_rows}
    change_map = {r["company_id"]: r["change_pct"] for r in market_rows}

    inv_shares = {
        r["company_id"]: r["shares"]
        for r in conn.execute("SELECT * FROM investments WHERE user_id=?", (uid,)).fetchall()
    }

    stocks_value = 0.0
    companies_value = 0.0
    market = []
    for comp in COMPANIES:
        cid = comp["id"]
        price = price_map.get(cid, comp["price"])
        shares = inv_shares.get(cid, 0)
        owned = cid in owned_ids
        market_cap = price * comp["shares_outstanding"]
        if owned:
            companies_value += market_cap
        else:
            stocks_value += shares * price
        market.append(
            {
                "id": cid,
                "name": comp["name"],
                "price": round(price, 2),
                "change": round(change_map.get(cid, 0.0), 2),
                "shares": shares,
                "shares_outstanding": comp["shares_outstanding"],
                "value": round(shares * price, 2),
                "market_cap": round(market_cap, 2),
                "owned": owned,
            }
        )

    net_worth = cash + stocks_value + companies_value + property_value

    # Cronologia
    tx_rows = conn.execute(
        "SELECT * FROM transactions WHERE user_id=? ORDER BY ts DESC LIMIT 100", (uid,)
    ).fetchall()
    history = [{"description": r["description"], "amount": r["amount"], "ts": r["ts"]} for r in tx_rows]

    # Achievement
    unlocked = {
        r["code"] for r in conn.execute("SELECT code FROM achievements WHERE user_id=?", (uid,)).fetchall()
    }
    ach_list = []
    for a in ACHIEVEMENTS:
        is_unlocked = a["code"] in unlocked
        ach_list.append(
            {
                "code": a["code"],
                "name": a["name"] if (is_unlocked or not a["hidden"]) else "???",
                "desc": a["desc"] if (is_unlocked or not a["hidden"]) else "Achievement segreto.",
                "hidden": a["hidden"],
                "unlocked": is_unlocked,
            }
        )

    return {
        "id": uid,
        "name": user["name"],
        "cash": round(cash, 2),
        "net_worth": round(net_worth, 2),
        "breakdown": {
            "cash": round(max(cash, 0), 2),
            "stocks": round(stocks_value, 2),
            "companies": round(companies_value, 2),
            "property": round(property_value, 2),
            "objects": round(objects_value, 2),
            "debt": round(min(cash, 0), 2),
        },
        "inventory": inventory,
        "market": market,
        "history": history,
        "achievements": ach_list,
    }


def check_achievements(conn, uid):
    """Valuta gli achievement basati sullo stato corrente. Ritorna lista nuovi."""
    new = []
    user = database.get_user(conn, uid)
    cash = user["cash"]

    # calcolo net worth veloce
    state = compute_state(conn, uid)
    net = state["net_worth"]

    if cash <= 0:
        a = unlock(conn, uid, "POVERO")
        if a:
            new.append(a)
    if net >= 1_000_000:
        a = unlock(conn, uid, "RICCO")
        if a:
            new.append(a)
    if net >= 10_000_000:
        a = unlock(conn, uid, "MILIONARIO")
        if a:
            new.append(a)

    # oggetti inutili
    useless_rows = conn.execute(
        "SELECT category, price FROM inventory WHERE user_id=?", (uid,)
    ).fetchall()
    useless_count = sum(1 for r in useless_rows if r["category"] in USELESS_CATEGORIES)
    useless_spend = sum(r["price"] for r in useless_rows if r["category"] in USELESS_CATEGORIES)
    if useless_count >= 100:
        a = unlock(conn, uid, "PERCHE")
        if a:
            new.append(a)
    if useless_spend >= 10000:
        a = unlock(conn, uid, "INUTILE")
        if a:
            new.append(a)

    # collezionista: 50 oggetti diversi
    distinct = conn.execute(
        "SELECT COUNT(DISTINCT product_id) AS n FROM inventory WHERE user_id=?", (uid,)
    ).fetchone()["n"]
    if distinct >= 50:
        a = unlock(conn, uid, "COLLEZIONISTA")
        if a:
            new.append(a)

    # capitalista: 10% di un'azienda
    for inv in conn.execute("SELECT * FROM investments WHERE user_id=?", (uid,)).fetchall():
        comp = COMPANIES_BY_ID.get(inv["company_id"])
        if comp and inv["shares"] >= 0.10 * comp["shares_outstanding"]:
            a = unlock(conn, uid, "CAPITALISTA")
            if a:
                new.append(a)
            break

    return new


# ---------------------------------------------------------------------------
# Pagine
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()[:40]
    if not name:
        return jsonify({"error": "Serve un nome."}), 400
    uid = database.create_user(name)
    conn = database.get_conn()
    state = compute_state(conn, uid)
    conn.close()
    return jsonify(state)


@app.route("/api/state")
def api_state():
    uid = request.args.get("pid", "")
    conn = database.get_conn()
    state = compute_state(conn, uid)
    conn.close()
    if not state:
        return jsonify({"error": "not_found"}), 404
    return jsonify(state)


@app.route("/api/catalog")
def api_catalog():
    return jsonify({"categories": CATEGORIES, "products": PRODUCTS})


@app.route("/api/buy", methods=["POST"])
def api_buy():
    data = request.get_json(force=True) or {}
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
    # Il debito è consentito: puoi comprare andando in negativo.
    conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (price, uid))
    conn.execute(
        "INSERT INTO inventory (user_id, product_id, name, price, category, ts) VALUES (?,?,?,?,?,?)",
        (uid, product_id, product["name"], price, product["category"], time.time()),
    )
    add_transaction(conn, uid, product["name"], -price)

    went_into_debt = cash >= 0 and (cash - price) < 0
    new_ach = check_achievements(conn, uid)
    conn.commit()
    phrase = random.choice(BUY_PHRASES).format(name=user["name"])
    state = compute_state(conn, uid)
    conn.close()
    return jsonify(
        {
            "ok": True,
            "phrase": phrase,
            "went_into_debt": went_into_debt,
            "new_achievements": new_ach,
            "state": state,
        }
    )


@app.route("/api/buy_stock", methods=["POST"])
def api_buy_stock():
    data = request.get_json(force=True) or {}
    uid = data.get("pid", "")
    cid = data.get("company_id", "")
    shares = int(data.get("shares", 1) or 1)
    if shares < 1:
        shares = 1
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    comp = COMPANIES_BY_ID.get(cid)
    if not user or not comp:
        conn.close()
        return jsonify({"error": "not_found"}), 404
    owned = conn.execute(
        "SELECT 1 FROM companies_owned WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()
    if owned:
        conn.close()
        return jsonify({"error": "Possiedi già l'intera azienda."}), 400

    mrow = conn.execute(
        "SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()
    price = mrow["price"]
    cost = price * shares
    if user["cash"] < cost:
        conn.close()
        return jsonify({"ok": False, "error": "Non puoi permettertelo."}), 400

    conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cost, uid))
    existing = conn.execute(
        "SELECT shares FROM investments WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()
    first_stock = existing is None or existing["shares"] == 0
    if existing:
        conn.execute(
            "UPDATE investments SET shares = shares + ?, last_buy_ts = ? WHERE user_id=? AND company_id=?",
            (shares, time.time(), uid, cid),
        )
    else:
        conn.execute(
            "INSERT INTO investments (user_id, company_id, shares, last_buy_ts) VALUES (?,?,?,?)",
            (uid, cid, shares, time.time()),
        )
    add_transaction(conn, uid, f"{shares}x {comp['name']} (azioni)", -cost)

    new_ach = []
    if first_stock:
        a = unlock(conn, uid, "INVESTITORE")
        if a:
            new_ach.append(a)
    new_ach += check_achievements(conn, uid)
    conn.commit()
    state = compute_state(conn, uid)
    conn.close()
    return jsonify({"ok": True, "new_achievements": new_ach, "state": state})


@app.route("/api/sell_stock", methods=["POST"])
def api_sell_stock():
    data = request.get_json(force=True) or {}
    uid = data.get("pid", "")
    cid = data.get("company_id", "")
    shares = int(data.get("shares", 1) or 1)
    if shares < 1:
        shares = 1
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    comp = COMPANIES_BY_ID.get(cid)
    inv = conn.execute(
        "SELECT * FROM investments WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()
    if not user or not comp or not inv or inv["shares"] < shares:
        conn.close()
        return jsonify({"error": "Non hai abbastanza azioni."}), 400

    mrow = conn.execute(
        "SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()
    price = mrow["price"]
    gain = price * shares
    conn.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (gain, uid))
    conn.execute(
        "UPDATE investments SET shares = shares - ? WHERE user_id=? AND company_id=?",
        (shares, uid, cid),
    )
    add_transaction(conn, uid, f"Venduto {shares}x {comp['name']}", gain)

    new_ach = []
    if time.time() - inv["last_buy_ts"] <= 10:
        a = unlock(conn, uid, "CAMBIATO_IDEA")
        if a:
            new_ach.append(a)
    new_ach += check_achievements(conn, uid)
    conn.commit()
    state = compute_state(conn, uid)
    conn.close()
    return jsonify({"ok": True, "new_achievements": new_ach, "state": state})


@app.route("/api/buy_company", methods=["POST"])
def api_buy_company():
    data = request.get_json(force=True) or {}
    uid = data.get("pid", "")
    cid = data.get("company_id", "")
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    comp = COMPANIES_BY_ID.get(cid)
    if not user or not comp:
        conn.close()
        return jsonify({"error": "not_found"}), 404
    already = conn.execute(
        "SELECT 1 FROM companies_owned WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()
    if already:
        conn.close()
        return jsonify({"error": "Già tua."}), 400

    price = conn.execute(
        "SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)
    ).fetchone()["price"]
    market_cap = price * comp["shares_outstanding"]
    if user["cash"] < market_cap:
        conn.close()
        return jsonify({"ok": False, "error": "Non puoi permettertelo."}), 400

    conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (market_cap, uid))
    conn.execute(
        "INSERT INTO companies_owned (user_id, company_id, bought_at) VALUES (?,?,?)",
        (uid, cid, time.time()),
    )
    add_transaction(conn, uid, f"Acquisto azienda: {comp['name']}", -market_cap)
    new_ach = []
    a = unlock(conn, uid, "MONOPOLIO")
    if a:
        new_ach.append(a)
    new_ach += check_achievements(conn, uid)
    conn.commit()
    state = compute_state(conn, uid)
    conn.close()
    return jsonify(
        {
            "ok": True,
            "company_name": comp["name"],
            "new_achievements": new_ach,
            "state": state,
        }
    )


@app.route("/api/tick", methods=["POST"])
def api_tick():
    """Avanza il mercato, applica interessi ed eventi casuali."""
    data = request.get_json(force=True) or {}
    uid = data.get("pid", "")
    conn = database.get_conn()
    user = database.get_user(conn, uid)
    if not user:
        conn.close()
        return jsonify({"error": "not_found"}), 404

    events = []

    # 1) Random walk dei prezzi
    for comp in COMPANIES:
        cid = comp["id"]
        row = conn.execute(
            "SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, cid)
        ).fetchone()
        old = row["price"]
        drift = random.gauss(0, comp["volatility"])
        new = max(0.5, old * (1 + drift))
        change = (new / old - 1) * 100 if old else 0
        conn.execute(
            "UPDATE market SET price=?, change_pct=? WHERE user_id=? AND company_id=?",
            (new, change, uid, cid),
        )

    # 2) Evento di mercato (raro)
    if random.random() < 0.22:
        comp = random.choice(COMPANIES)
        ev = random.choice(comp["events"])
        row = conn.execute(
            "SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, comp["id"])
        ).fetchone()
        old = row["price"]
        new = max(0.5, old * (1 + ev["pct"] / 100))
        change = (new / old - 1) * 100 if old else 0
        conn.execute(
            "UPDATE market SET price=?, change_pct=? WHERE user_id=? AND company_id=?",
            (new, change, uid, comp["id"]),
        )
        events.append(
            {"type": "market", "company": comp["name"], "text": ev["text"], "pct": ev["pct"]}
        )

    # 3) Entrate dalle aziende possedute
    owned = conn.execute(
        "SELECT company_id FROM companies_owned WHERE user_id=?", (uid,)
    ).fetchall()
    for o in owned:
        comp = COMPANIES_BY_ID.get(o["company_id"])
        if comp and random.random() < 0.25:
            row = conn.execute(
                "SELECT price FROM market WHERE user_id=? AND company_id=?", (uid, comp["id"])
            ).fetchone()
            income = round(row["price"] * comp["shares_outstanding"] * comp["income"], 2)
            if income > 0:
                conn.execute("UPDATE users SET cash = cash + ? WHERE id=?", (income, uid))
                add_transaction(conn, uid, f"Entrate da {comp['name']}", income)
                events.append(
                    {"type": "income", "text": f"{comp['name']} ti ha fruttato denaro.", "amount": income}
                )

    # 4) Interessi sul debito
    user = database.get_user(conn, uid)
    if user["cash"] < 0 and random.random() < 0.5:
        interest = round(abs(user["cash"]) * 0.02, 2)
        if interest > 0:
            conn.execute("UPDATE users SET cash = cash - ? WHERE id=?", (interest, uid))
            add_transaction(conn, uid, "Gli interessi hanno deciso di esistere.", -interest)
            events.append({"type": "interest", "text": "Gli interessi hanno deciso di esistere.", "amount": -interest})

    # 5) Evento casuale del giocatore (raro)
    if random.random() < 0.15:
        has_company = len(owned) > 0
        pool = [e for e in PLAYER_EVENTS if not e.get("needs_company") or has_company]
        ev = random.choice(pool)
        amount = ev["amount"]
        conn.execute("UPDATE users SET cash = cash + ? WHERE id=?", (amount, uid))
        text = ev["text"].format(name=user["name"])
        add_transaction(conn, uid, text, amount)
        events.append({"type": "player", "text": text, "amount": amount})

    new_ach = check_achievements(conn, uid)
    conn.commit()
    state = compute_state(conn, uid)
    conn.close()
    return jsonify({"ok": True, "events": events, "new_achievements": new_ach, "state": state})


if __name__ == "__main__":
    database.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
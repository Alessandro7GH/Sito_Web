"""Aziende immaginarie quotate in SOMETHING BANK.

Ogni azienda:
  id, name, price (prezzo iniziale per azione),
  volatility (oscillazione random per tick),
  shares_outstanding (azioni totali -> market cap),
  income (entrata periodica quando possiedi l'azienda),
  events (lista di eventi di mercato: testo + variazione %).

market_cap = price * shares_outstanding
"""

COMPANIES = [
    {
        "id": "pizzabox",
        "name": "PIZZABOX",
        "price": 120.0,
        "volatility": 0.03,
        "shares_outstanding": 20000,   # market cap iniziale: 2.400.000
        "income": 0.004,
        "events": [
            {"text": "Un influencer ha detto che la pizza è buona.", "pct": 18.0},
            {"text": "Nuovo gusto: ananas obbligatorio.", "pct": -9.0},
            {"text": "Consegna in 3 secondi. Nessuno sa come.", "pct": 12.0},
            {"text": "Hanno dimenticato di mettere la pizza nella scatola.", "pct": -6.5},
        ],
    },
    {
        "id": "catenergy",
        "name": "CAT ENERGY",
        "price": 310.0,
        "volatility": 0.06,
        "shares_outstanding": 15000,
        "income": 0.006,
        "events": [
            {"text": "Milioni di gatti hanno approvato il prodotto.", "pct": 17.4},
            {"text": "È stato scoperto che i gatti non bevono energia.", "pct": -43.0},
            {"text": "Un gatto è diventato CEO.", "pct": 22.0},
            {"text": "I gatti dormono invece di lavorare.", "pct": -11.0},
        ],
    },
    {
        "id": "boringbank",
        "name": "BORING BANK",
        "price": 91.0,
        "volatility": 0.004,
        "shares_outstanding": 40000,
        "income": 0.002,
        "events": [
            {"text": "Non è successo niente.", "pct": 0.1},
            {"text": "Ancora niente.", "pct": -0.1},
            {"text": "Una riunione è finita in orario.", "pct": 0.3},
            {"text": "Qualcuno ha sbadigliato in borsa.", "pct": -0.2},
        ],
    },
    {
        "id": "mooninc",
        "name": "MOON INC.",
        "price": 4800.0,
        "volatility": 0.09,
        "shares_outstanding": 3000,
        "income": 0.008,
        "events": [
            {"text": "Hanno promesso di comprare la Luna.", "pct": 26.0},
            {"text": "La Luna non era in vendita.", "pct": -12.7},
            {"text": "Razzo lanciato con successo (nel garage).", "pct": 14.0},
            {"text": "Il razzo è tornato indietro da solo.", "pct": -19.0},
        ],
    },
    {
        "id": "megatoothbrush",
        "name": "MEGA TOOTHBRUSH",
        "price": 73.0,
        "volatility": 0.025,
        "shares_outstanding": 25000,
        "income": 0.003,
        "events": [
            {"text": "Denti più bianchi del previsto.", "pct": 9.0},
            {"text": "Lo spazzolino era troppo grande per la bocca.", "pct": -2.1},
            {"text": "Adottato da tutti i dentisti immaginari.", "pct": 13.0},
            {"text": "Richiamo prodotto: vibrava troppo.", "pct": -8.0},
        ],
    },
    {
        "id": "sassocorp",
        "name": "SASSO CORP",
        "price": 15.0,
        "volatility": 0.05,
        "shares_outstanding": 50000,
        "income": 0.002,
        "events": [
            {"text": "I sassi sono di nuovo di moda.", "pct": 30.0},
            {"text": "Qualcuno ha capito che sono solo sassi.", "pct": -25.0},
            {"text": "Edizione limitata: sasso quadrato.", "pct": 16.0},
        ],
    },
    {
        "id": "pixellabs",
        "name": "PIXEL LABS",
        "price": 640.0,
        "volatility": 0.07,
        "shares_outstanding": 8000,
        "income": 0.005,
        "events": [
            {"text": "Hanno venduto un pixel per un milione.", "pct": 21.0},
            {"text": "Il pixel era leggermente storto.", "pct": -14.0},
            {"text": "Nuova risoluzione: infinita.", "pct": 11.0},
        ],
    },
    {
        "id": "nothingltd",
        "name": "NOTHING LTD",
        "price": 42.0,
        "volatility": 0.02,
        "shares_outstanding": 30000,
        "income": 0.001,
        "events": [
            {"text": "Hanno prodotto nulla, come promesso.", "pct": 5.0},
            {"text": "Il nulla ha deluso gli investitori.", "pct": -7.0},
            {"text": "Espansione: ora fanno nulla in due Paesi.", "pct": 8.0},
        ],
    },
]

COMPANIES_BY_ID = {c["id"]: c for c in COMPANIES}
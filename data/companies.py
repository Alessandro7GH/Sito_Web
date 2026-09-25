"""Aziende immaginarie quotate in SOMETHING BANK (eventi bilingue IT/EN)."""

COMPANIES = [
    {
        "id": "pizzabox", "name": "PIZZABOX", "price": 120.0, "volatility": 0.03,
        "shares_outstanding": 20000, "income": 0.004,
        "events": [
            {"it": "Un influencer ha detto che la pizza è buona.", "en": "An influencer said pizza is good.", "pct": 18.0},
            {"it": "Nuovo gusto: ananas obbligatorio.", "en": "New flavour: pineapple mandatory.", "pct": -9.0},
            {"it": "Consegna in 3 secondi. Nessuno sa come.", "en": "3-second delivery. Nobody knows how.", "pct": 12.0},
            {"it": "Hanno dimenticato di mettere la pizza nella scatola.", "en": "They forgot to put pizza in the box.", "pct": -6.5},
        ],
    },
    {
        "id": "catenergy", "name": "CAT ENERGY", "price": 310.0, "volatility": 0.06,
        "shares_outstanding": 15000, "income": 0.006,
        "events": [
            {"it": "Milioni di gatti hanno approvato il prodotto.", "en": "Millions of cats approved the product.", "pct": 17.4},
            {"it": "È stato scoperto che i gatti non bevono energia.", "en": "Turns out cats don't drink energy.", "pct": -43.0},
            {"it": "Un gatto è diventato CEO.", "en": "A cat became CEO.", "pct": 22.0},
            {"it": "I gatti dormono invece di lavorare.", "en": "Cats sleep instead of working.", "pct": -11.0},
        ],
    },
    {
        "id": "boringbank", "name": "BORING BANK", "price": 91.0, "volatility": 0.004,
        "shares_outstanding": 40000, "income": 0.002,
        "events": [
            {"it": "Non è successo niente.", "en": "Nothing happened.", "pct": 0.1},
            {"it": "Ancora niente.", "en": "Still nothing.", "pct": -0.1},
            {"it": "Una riunione è finita in orario.", "en": "A meeting ended on time.", "pct": 0.3},
            {"it": "Qualcuno ha sbadigliato in borsa.", "en": "Someone yawned on the trading floor.", "pct": -0.2},
        ],
    },
    {
        "id": "mooninc", "name": "MOON INC.", "price": 4800.0, "volatility": 0.09,
        "shares_outstanding": 3000, "income": 0.008,
        "events": [
            {"it": "Hanno promesso di comprare la Luna.", "en": "They promised to buy the Moon.", "pct": 26.0},
            {"it": "La Luna non era in vendita.", "en": "The Moon wasn't for sale.", "pct": -12.7},
            {"it": "Razzo lanciato con successo (nel garage).", "en": "Rocket launched successfully (in the garage).", "pct": 14.0},
            {"it": "Il razzo è tornato indietro da solo.", "en": "The rocket came back on its own.", "pct": -19.0},
        ],
    },
    {
        "id": "megatoothbrush", "name": "MEGA TOOTHBRUSH", "price": 73.0, "volatility": 0.025,
        "shares_outstanding": 25000, "income": 0.003,
        "events": [
            {"it": "Denti più bianchi del previsto.", "en": "Whiter teeth than expected.", "pct": 9.0},
            {"it": "Lo spazzolino era troppo grande per la bocca.", "en": "The toothbrush was too big for the mouth.", "pct": -2.1},
            {"it": "Adottato da tutti i dentisti immaginari.", "en": "Adopted by all imaginary dentists.", "pct": 13.0},
            {"it": "Richiamo prodotto: vibrava troppo.", "en": "Product recall: it vibrated too much.", "pct": -8.0},
        ],
    },
    {
        "id": "sassocorp", "name": "SASSO CORP", "price": 15.0, "volatility": 0.05,
        "shares_outstanding": 50000, "income": 0.002,
        "events": [
            {"it": "I sassi sono di nuovo di moda.", "en": "Rocks are trendy again.", "pct": 30.0},
            {"it": "Qualcuno ha capito che sono solo sassi.", "en": "Someone realised they're just rocks.", "pct": -25.0},
            {"it": "Edizione limitata: sasso quadrato.", "en": "Limited edition: square rock.", "pct": 16.0},
        ],
    },
    {
        "id": "pixellabs", "name": "PIXEL LABS", "price": 640.0, "volatility": 0.07,
        "shares_outstanding": 8000, "income": 0.005,
        "events": [
            {"it": "Hanno venduto un pixel per un milione.", "en": "They sold a pixel for a million.", "pct": 21.0},
            {"it": "Il pixel era leggermente storto.", "en": "The pixel was slightly crooked.", "pct": -14.0},
            {"it": "Nuova risoluzione: infinita.", "en": "New resolution: infinite.", "pct": 11.0},
        ],
    },
    {
        "id": "nothingltd", "name": "NOTHING LTD", "price": 42.0, "volatility": 0.02,
        "shares_outstanding": 30000, "income": 0.001,
        "events": [
            {"it": "Hanno prodotto nulla, come promesso.", "en": "They produced nothing, as promised.", "pct": 5.0},
            {"it": "Il nulla ha deluso gli investitori.", "en": "The nothing disappointed investors.", "pct": -7.0},
            {"it": "Espansione: ora fanno nulla in due Paesi.", "en": "Expansion: now doing nothing in two countries.", "pct": 8.0},
        ],
    },
]

COMPANIES_BY_ID = {c["id"]: c for c in COMPANIES}
"""Catalogo prodotti di SOMETHING BANK.

Ogni prodotto: id, name, price, description, category.
Le categorie "Oggetti inutili" e "Cose assurde" contano come "inutili"
per gli achievement.
"""

USELESS_CATEGORIES = {"Oggetti inutili", "Cose assurde"}
PROPERTY_CATEGORIES = {"Case"}

CATEGORIES = [
    "Cibo",
    "Tecnologia",
    "Vestiti",
    "Auto",
    "Case",
    "Viaggi",
    "Esperienze",
    "Intrattenimento",
    "Oggetti inutili",
    "Aziende",
    "Cose assurde",
]

PRODUCTS = [
    # --- Cibo ---
    {"id": "pizza", "name": "Pizza", "price": 8, "description": "Rotonda. Calda. Perfetta.", "category": "Cibo"},
    {"id": "caffe", "name": "Caffè", "price": 2, "description": "Il carburante dell'umanità.", "category": "Cibo"},
    {"id": "hamburger", "name": "Hamburger gigante", "price": 15, "description": "Non entrerà mai in bocca.", "category": "Cibo"},
    {"id": "sushi", "name": "Sushi", "price": 45, "description": "Pesce crudo, prezzi cotti.", "category": "Cibo"},
    {"id": "torta", "name": "Torta intera", "price": 30, "description": "Per te. Tutta per te.", "category": "Cibo"},
    {"id": "cioccolato_oro", "name": "Cioccolato ricoperto d'oro", "price": 1200, "description": "Commestibile. Costoso. Discutibile.", "category": "Cibo"},

    # --- Tecnologia ---
    {"id": "cuffie", "name": "Cuffie", "price": 80, "description": "Per non sentire il mondo.", "category": "Tecnologia"},
    {"id": "smartphone", "name": "Smartphone", "price": 1000, "description": "Lo guarderai per 6 ore al giorno.", "category": "Tecnologia"},
    {"id": "laptop", "name": "Laptop", "price": 1800, "description": "Per lavorare. Teoricamente.", "category": "Tecnologia"},
    {"id": "tv", "name": "TV enorme", "price": 3500, "description": "Non entra in nessuna stanza.", "category": "Tecnologia"},
    {"id": "drone", "name": "Drone", "price": 600, "description": "Lo perderai al primo volo.", "category": "Tecnologia"},
    {"id": "robot", "name": "Robot domestico", "price": 25000, "description": "Ti giudicherà in silenzio.", "category": "Tecnologia"},

    # --- Vestiti ---
    {"id": "tshirt", "name": "T-shirt", "price": 25, "description": "Una maglietta. Rivoluzionario.", "category": "Vestiti"},
    {"id": "scarpe", "name": "Scarpe da ginnastica", "price": 150, "description": "Per correre. O per stare fermi.", "category": "Vestiti"},
    {"id": "giacca", "name": "Giacca elegante", "price": 400, "description": "Per sembrare importante.", "category": "Vestiti"},
    {"id": "orologio", "name": "Orologio di lusso", "price": 12000, "description": "Dice l'ora. Come tutti gli altri.", "category": "Vestiti"},
    {"id": "cappello", "name": "Cappello assurdo", "price": 90, "description": "Nessuno saprà perché.", "category": "Vestiti"},

    # --- Auto ---
    {"id": "bicicletta", "name": "Bicicletta", "price": 900, "description": "Ecologica. Faticosa.", "category": "Auto"},
    {"id": "scooter", "name": "Scooter", "price": 3000, "description": "Veloce quanto basta.", "category": "Auto"},
    {"id": "macchina", "name": "Macchina", "price": 30000, "description": "Quattro ruote e un sogno.", "category": "Auto"},
    {"id": "suv", "name": "SUV", "price": 65000, "description": "Grande. Molto grande.", "category": "Auto"},
    {"id": "supercar", "name": "Supercar", "price": 250000, "description": "Rossa. Ovviamente rossa.", "category": "Auto"},
    {"id": "jet", "name": "Jet privato", "price": 15000000, "description": "Il traffico non esiste più.", "category": "Auto"},

    # --- Case ---
    {"id": "monolocale", "name": "Monolocale", "price": 90000, "description": "Piccolo ma tuo.", "category": "Case"},
    {"id": "casa", "name": "Casa", "price": 350000, "description": "Con giardino immaginario.", "category": "Case"},
    {"id": "villa", "name": "Villa", "price": 2500000, "description": "Troppe stanze da pulire.", "category": "Case"},
    {"id": "castello", "name": "Castello", "price": 12000000, "description": "Fantasmi inclusi.", "category": "Case"},
    {"id": "isola", "name": "Isola", "price": 8000000, "description": "Nessun vicino. Mai.", "category": "Case"},

    # --- Viaggi ---
    {"id": "weekend", "name": "Weekend fuori", "price": 500, "description": "Due giorni di finta pace.", "category": "Viaggi"},
    {"id": "vacanza", "name": "Vacanza di lusso", "price": 8000, "description": "Foto per far invidia.", "category": "Viaggi"},
    {"id": "spazio", "name": "Viaggio nello spazio", "price": 500000, "description": "Sopra tutti. Letteralmente.", "category": "Viaggi"},
    {"id": "giro_mondo", "name": "Giro del mondo", "price": 40000, "description": "Tornerai stanco uguale.", "category": "Viaggi"},

    # --- Esperienze ---
    {"id": "concerto", "name": "Concerto in prima fila", "price": 300, "description": "Urlerai fino a perdere la voce.", "category": "Esperienze"},
    {"id": "cena_stellata", "name": "Cena stellata", "price": 700, "description": "Piatti piccoli, conti enormi.", "category": "Esperienze"},
    {"id": "corso_cucina", "name": "Corso di cucina", "price": 250, "description": "Brucerai comunque tutto.", "category": "Esperienze"},
    {"id": "paracadute", "name": "Lancio col paracadute", "price": 350, "description": "Adrenalina e rimpianti.", "category": "Esperienze"},

    # --- Intrattenimento ---
    {"id": "console", "name": "Console di gioco", "price": 500, "description": "Addio tempo libero.", "category": "Intrattenimento"},
    {"id": "biliardo", "name": "Tavolo da biliardo", "price": 2000, "description": "Occuperà tutto il salotto.", "category": "Intrattenimento"},
    {"id": "cinema_casa", "name": "Cinema in casa", "price": 15000, "description": "Popcorn non inclusi.", "category": "Intrattenimento"},
    {"id": "parco_giochi", "name": "Parco giochi personale", "price": 400000, "description": "Solo per te. Vuoto.", "category": "Intrattenimento"},

    # --- Oggetti inutili ---
    {"id": "sasso", "name": "Un sasso", "price": 3, "description": "È un sasso.", "category": "Oggetti inutili"},
    {"id": "sasso_migliore", "name": "Un sasso leggermente migliore", "price": 7, "description": "Leggermente migliore. Non chiedere.", "category": "Oggetti inutili"},
    {"id": "scatola_vuota", "name": "Una scatola vuota", "price": 19, "description": "Contiene aria selezionata.", "category": "Oggetti inutili"},
    {"id": "scatola_premium", "name": "Una scatola vuota premium", "price": 49, "description": "Aria premium.", "category": "Oggetti inutili"},
    {"id": "pixel", "name": "Un pixel", "price": 1, "description": "Un singolo pixel. Tuo.", "category": "Oggetti inutili"},
    {"id": "pixel_oro", "name": "Un pixel dorato", "price": 500, "description": "Lo stesso pixel, ma dorato.", "category": "Oggetti inutili"},
    {"id": "foto_sasso", "name": "Una foto di un sasso", "price": 12, "description": "Non è nemmeno il sasso vero.", "category": "Oggetti inutili"},
    {"id": "sedia_inutile", "name": "Una sedia che non puoi usare", "price": 250, "description": "Guardala e basta.", "category": "Oggetti inutili"},
    {"id": "pulsante", "name": "Un pulsante", "price": 5, "description": "Non fa niente.", "category": "Oggetti inutili"},
    {"id": "patata", "name": "Una patata", "price": 500, "description": "500 euro. Una patata.", "category": "Oggetti inutili"},

    # --- Aziende (mini-attività da collezione) ---
    {"id": "chiosco_limonate", "name": "Chiosco di limonate", "price": 1500, "description": "Il tuo impero comincia qui.", "category": "Aziende"},
    {"id": "food_truck", "name": "Food truck", "price": 45000, "description": "Cibo su ruote.", "category": "Aziende"},
    {"id": "lavanderia", "name": "Lavanderia a gettoni", "price": 120000, "description": "Sorprendentemente redditizia.", "category": "Aziende"},
    {"id": "fabbrica_calzini", "name": "Fabbrica di calzini spaiati", "price": 800000, "description": "Ne produce sempre uno solo.", "category": "Aziende"},

    # --- Cose assurde ---
    {"id": "nome_stella", "name": "Il nome di una stella", "price": 60, "description": "Non è ufficiale. Non lo è mai.", "category": "Cose assurde"},
    {"id": "nuvola", "name": "Una nuvola", "price": 9000, "description": "Certificato di proprietà incluso.", "category": "Cose assurde"},
    {"id": "eco", "name": "Un'eco", "price": 200, "description": "Un'eco. Un'eco. Un'eco.", "category": "Cose assurde"},
    {"id": "silenzio", "name": "Cinque minuti di silenzio", "price": 999, "description": "Estremamente rari.", "category": "Cose assurde"},
    {"id": "buco", "name": "Un buco", "price": 400, "description": "Il nulla, in vendita.", "category": "Cose assurde"},
    {"id": "mercoledi", "name": "La proprietà del mercoledì", "price": 1000000, "description": "Ogni mercoledì è tuo. Concettualmente.", "category": "Cose assurde"},
    {"id": "urlo", "name": "Un urlo in scatola", "price": 75, "description": "Aprila e scappa.", "category": "Cose assurde"},
]

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS}
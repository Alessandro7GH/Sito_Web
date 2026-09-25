"""Catalogo prodotti di SOMETHING BANK (bilingue IT/EN).

Ogni prodotto: id, name/name_en, description/description_en, price, category.
Le categorie "Oggetti inutili" e "Cose assurde" contano come "inutili"
per gli achievement. Le chiavi delle categorie restano in italiano (uso interno);
le etichette tradotte sono in CATEGORY_LABELS.
"""

USELESS_CATEGORIES = {"Oggetti inutili", "Cose assurde"}
PROPERTY_CATEGORIES = {"Case"}

# chiave interna -> etichette tradotte
CATEGORY_LABELS = {
    "Cibo": {"it": "Cibo", "en": "Food"},
    "Tecnologia": {"it": "Tecnologia", "en": "Technology"},
    "Vestiti": {"it": "Vestiti", "en": "Clothes"},
    "Auto": {"it": "Auto", "en": "Cars"},
    "Case": {"it": "Case", "en": "Houses"},
    "Viaggi": {"it": "Viaggi", "en": "Travel"},
    "Esperienze": {"it": "Esperienze", "en": "Experiences"},
    "Intrattenimento": {"it": "Intrattenimento", "en": "Entertainment"},
    "Oggetti inutili": {"it": "Oggetti inutili", "en": "Useless things"},
    "Aziende": {"it": "Aziende", "en": "Businesses"},
    "Cose assurde": {"it": "Cose assurde", "en": "Absurd things"},
}

CATEGORIES = list(CATEGORY_LABELS.keys())


def _p(pid, it_name, en_name, price, it_desc, en_desc, category):
    return {
        "id": pid,
        "name": it_name,
        "name_en": en_name,
        "price": price,
        "description": it_desc,
        "description_en": en_desc,
        "category": category,
    }


PRODUCTS = [
    # --- Cibo / Food ---
    _p("pizza", "Pizza", "Pizza", 8, "Rotonda. Calda. Perfetta.", "Round. Hot. Perfect.", "Cibo"),
    _p("caffe", "Caffè", "Coffee", 2, "Il carburante dell'umanità.", "Humanity's fuel.", "Cibo"),
    _p("hamburger", "Hamburger gigante", "Giant burger", 15, "Non entrerà mai in bocca.", "It will never fit in your mouth.", "Cibo"),
    _p("sushi", "Sushi", "Sushi", 45, "Pesce crudo, prezzi cotti.", "Raw fish, cooked prices.", "Cibo"),
    _p("torta", "Torta intera", "Whole cake", 30, "Per te. Tutta per te.", "For you. All of it.", "Cibo"),
    _p("cioccolato_oro", "Cioccolato ricoperto d'oro", "Gold-covered chocolate", 1200, "Commestibile. Costoso. Discutibile.", "Edible. Expensive. Questionable.", "Cibo"),

    # --- Tecnologia / Technology ---
    _p("cuffie", "Cuffie", "Headphones", 80, "Per non sentire il mondo.", "To not hear the world.", "Tecnologia"),
    _p("smartphone", "Smartphone", "Smartphone", 1000, "Lo guarderai per 6 ore al giorno.", "You'll stare at it 6 hours a day.", "Tecnologia"),
    _p("laptop", "Laptop", "Laptop", 1800, "Per lavorare. Teoricamente.", "For working. In theory.", "Tecnologia"),
    _p("tv", "TV enorme", "Huge TV", 3500, "Non entra in nessuna stanza.", "Fits in no room.", "Tecnologia"),
    _p("drone", "Drone", "Drone", 600, "Lo perderai al primo volo.", "You'll lose it on the first flight.", "Tecnologia"),
    _p("robot", "Robot domestico", "Home robot", 25000, "Ti giudicherà in silenzio.", "It will judge you silently.", "Tecnologia"),

    # --- Vestiti / Clothes ---
    _p("tshirt", "T-shirt", "T-shirt", 25, "Una maglietta. Rivoluzionario.", "A t-shirt. Revolutionary.", "Vestiti"),
    _p("scarpe", "Scarpe da ginnastica", "Sneakers", 150, "Per correre. O per stare fermi.", "To run. Or to stand still.", "Vestiti"),
    _p("giacca", "Giacca elegante", "Fancy jacket", 400, "Per sembrare importante.", "To look important.", "Vestiti"),
    _p("orologio", "Orologio di lusso", "Luxury watch", 12000, "Dice l'ora. Come tutti gli altri.", "Tells time. Like all the others.", "Vestiti"),
    _p("cappello", "Cappello assurdo", "Absurd hat", 90, "Nessuno saprà perché.", "Nobody will know why.", "Vestiti"),

    # --- Auto / Cars ---
    _p("bicicletta", "Bicicletta", "Bicycle", 900, "Ecologica. Faticosa.", "Eco-friendly. Tiring.", "Auto"),
    _p("scooter", "Scooter", "Scooter", 3000, "Veloce quanto basta.", "Fast enough.", "Auto"),
    _p("macchina", "Macchina", "Car", 30000, "Quattro ruote e un sogno.", "Four wheels and a dream.", "Auto"),
    _p("suv", "SUV", "SUV", 65000, "Grande. Molto grande.", "Big. Very big.", "Auto"),
    _p("supercar", "Supercar", "Supercar", 250000, "Rossa. Ovviamente rossa.", "Red. Obviously red.", "Auto"),
    _p("jet", "Jet privato", "Private jet", 15000000, "Il traffico non esiste più.", "Traffic no longer exists.", "Auto"),

    # --- Case / Houses ---
    _p("monolocale", "Monolocale", "Studio flat", 90000, "Piccolo ma tuo.", "Small but yours.", "Case"),
    _p("casa", "Casa", "House", 350000, "Con giardino immaginario.", "With an imaginary garden.", "Case"),
    _p("villa", "Villa", "Villa", 2500000, "Troppe stanze da pulire.", "Too many rooms to clean.", "Case"),
    _p("castello", "Castello", "Castle", 12000000, "Fantasmi inclusi.", "Ghosts included.", "Case"),
    _p("isola", "Isola", "Island", 8000000, "Nessun vicino. Mai.", "No neighbours. Ever.", "Case"),

    # --- Viaggi / Travel ---
    _p("weekend", "Weekend fuori", "Weekend away", 500, "Due giorni di finta pace.", "Two days of fake peace.", "Viaggi"),
    _p("vacanza", "Vacanza di lusso", "Luxury holiday", 8000, "Foto per far invidia.", "Photos to make people jealous.", "Viaggi"),
    _p("spazio", "Viaggio nello spazio", "Space trip", 500000, "Sopra tutti. Letteralmente.", "Above everyone. Literally.", "Viaggi"),
    _p("giro_mondo", "Giro del mondo", "Round-the-world trip", 40000, "Tornerai stanco uguale.", "You'll come back just as tired.", "Viaggi"),

    # --- Esperienze / Experiences ---
    _p("concerto", "Concerto in prima fila", "Front-row concert", 300, "Urlerai fino a perdere la voce.", "You'll scream until you lose your voice.", "Esperienze"),
    _p("cena_stellata", "Cena stellata", "Michelin dinner", 700, "Piatti piccoli, conti enormi.", "Tiny plates, huge bills.", "Esperienze"),
    _p("corso_cucina", "Corso di cucina", "Cooking class", 250, "Brucerai comunque tutto.", "You'll burn everything anyway.", "Esperienze"),
    _p("paracadute", "Lancio col paracadute", "Skydiving jump", 350, "Adrenalina e rimpianti.", "Adrenaline and regrets.", "Esperienze"),

    # --- Intrattenimento / Entertainment ---
    _p("console", "Console di gioco", "Game console", 500, "Addio tempo libero.", "Goodbye free time.", "Intrattenimento"),
    _p("biliardo", "Tavolo da biliardo", "Pool table", 2000, "Occuperà tutto il salotto.", "It'll take up the whole living room.", "Intrattenimento"),
    _p("cinema_casa", "Cinema in casa", "Home cinema", 15000, "Popcorn non inclusi.", "Popcorn not included.", "Intrattenimento"),
    _p("parco_giochi", "Parco giochi personale", "Personal playground", 400000, "Solo per te. Vuoto.", "Just for you. Empty.", "Intrattenimento"),

    # --- Oggetti inutili / Useless things ---
    _p("sasso", "Un sasso", "A rock", 3, "È un sasso.", "It's a rock.", "Oggetti inutili"),
    _p("sasso_migliore", "Un sasso leggermente migliore", "A slightly better rock", 7, "Leggermente migliore. Non chiedere.", "Slightly better. Don't ask.", "Oggetti inutili"),
    _p("scatola_vuota", "Una scatola vuota", "An empty box", 19, "Contiene aria selezionata.", "Contains selected air.", "Oggetti inutili"),
    _p("scatola_premium", "Una scatola vuota premium", "A premium empty box", 49, "Aria premium.", "Premium air.", "Oggetti inutili"),
    _p("pixel", "Un pixel", "A pixel", 1, "Un singolo pixel. Tuo.", "A single pixel. Yours.", "Oggetti inutili"),
    _p("pixel_oro", "Un pixel dorato", "A golden pixel", 500, "Lo stesso pixel, ma dorato.", "The same pixel, but golden.", "Oggetti inutili"),
    _p("foto_sasso", "Una foto di un sasso", "A photo of a rock", 12, "Non è nemmeno il sasso vero.", "It's not even the real rock.", "Oggetti inutili"),
    _p("sedia_inutile", "Una sedia che non puoi usare", "A chair you can't use", 250, "Guardala e basta.", "Just look at it.", "Oggetti inutili"),
    _p("pulsante", "Un pulsante", "A button", 5, "Non fa niente.", "It does nothing.", "Oggetti inutili"),
    _p("patata", "Una patata", "A potato", 500, "500 euro. Una patata.", "500 euros. A potato.", "Oggetti inutili"),

    # --- Aziende / Businesses ---
    _p("chiosco_limonate", "Chiosco di limonate", "Lemonade stand", 1500, "Il tuo impero comincia qui.", "Your empire starts here.", "Aziende"),
    _p("food_truck", "Food truck", "Food truck", 45000, "Cibo su ruote.", "Food on wheels.", "Aziende"),
    _p("lavanderia", "Lavanderia a gettoni", "Laundromat", 120000, "Sorprendentemente redditizia.", "Surprisingly profitable.", "Aziende"),
    _p("fabbrica_calzini", "Fabbrica di calzini spaiati", "Odd-sock factory", 800000, "Ne produce sempre uno solo.", "It always makes just one.", "Aziende"),

    # --- Cose assurde / Absurd things ---
    _p("nome_stella", "Il nome di una stella", "The name of a star", 60, "Non è ufficiale. Non lo è mai.", "It's not official. It never is.", "Cose assurde"),
    _p("nuvola", "Una nuvola", "A cloud", 9000, "Certificato di proprietà incluso.", "Ownership certificate included.", "Cose assurde"),
    _p("eco", "Un'eco", "An echo", 200, "Un'eco. Un'eco. Un'eco.", "An echo. An echo. An echo.", "Cose assurde"),
    _p("silenzio", "Cinque minuti di silenzio", "Five minutes of silence", 999, "Estremamente rari.", "Extremely rare.", "Cose assurde"),
    _p("buco", "Un buco", "A hole", 400, "Il nulla, in vendita.", "Nothingness, for sale.", "Cose assurde"),
    _p("mercoledi", "La proprietà del mercoledì", "Ownership of Wednesday", 1000000, "Ogni mercoledì è tuo. Concettualmente.", "Every Wednesday is yours. Conceptually.", "Cose assurde"),
    _p("urlo", "Un urlo in scatola", "A scream in a box", 75, "Aprila e scappa.", "Open it and run.", "Cose assurde"),
]

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS}
"""
uae_market.py
--------------
This file stores information about where to buy supplements in the UAE.
It is a simple dictionary — no calculations or logic, just data.
Each store entry includes a direct URL for clickable links in the app.
"""

UAE_MARKET = {

    "Whey Protein": {
        "tip": "Widely available across UAE. GNC and Life Pharmacy carry the most options.",
        "stores": [
            {"name": "GNC UAE",              "url": "www.gnc.ae",                   "location": "Dubai Mall, Mall of Emirates, Abu Dhabi"},
            {"name": "Life Pharmacy",         "url": "www.lifepharmacy.com",          "location": "500+ branches across UAE"},
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",      "location": "Dubai and Abu Dhabi"},
            {"name": "Amazon.ae",             "url": "www.amazon.ae/s?k=whey+protein","location": "Online - delivers across UAE"},
            {"name": "iHerb",                 "url": "ae.iherb.com",                 "location": "Online - ships to UAE"},
            {"name": "MyProtein UAE",         "url": "www.myprotein.com/ae",          "location": "Online - ships to UAE"},
        ],
        "brands": [
            {"brand": "Optimum Nutrition", "product": "Gold Standard Whey",  "price_aed": "180-320"},
            {"brand": "MyProtein",         "product": "Impact Whey Protein", "price_aed": "150-280"},
            {"brand": "MuscleTech",        "product": "Nitro-Tech Whey",     "price_aed": "200-350"},
        ],
    },

    "Creatine Monohydrate": {
        "tip": "One of the cheapest supplements available. MyProtein UAE offers the best value.",
        "stores": [
            {"name": "GNC UAE",              "url": "www.gnc.ae",                       "location": "Major malls across UAE"},
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",          "location": "Dubai and Abu Dhabi"},
            {"name": "Amazon.ae",             "url": "www.amazon.ae/s?k=creatine",        "location": "Online - UAE delivery"},
            {"name": "iHerb",                 "url": "ae.iherb.com",                     "location": "Online - ships to UAE"},
            {"name": "MyProtein UAE",         "url": "www.myprotein.com/ae",              "location": "Online - ships to UAE"},
        ],
        "brands": [
            {"brand": "Optimum Nutrition", "product": "Micronised Creatine",  "price_aed": "80-140"},
            {"brand": "MyProtein",         "product": "Creatine Monohydrate", "price_aed": "60-110"},
            {"brand": "BioTechUSA",        "product": "100% Creatine",        "price_aed": "70-130"},
        ],
    },

    "Multivitamin & Mineral Complex": {
        "tip": "Available at every pharmacy in UAE. Centrum is the most affordable option.",
        "stores": [
            {"name": "Life Pharmacy",         "url": "www.lifepharmacy.com",     "location": "500+ branches across UAE"},
            {"name": "Boots UAE",             "url": "www.boots.ae",             "location": "Dubai and Abu Dhabi"},
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",  "location": "Dubai and Abu Dhabi"},
            {"name": "Carrefour UAE",         "url": "www.carrefouruae.com",      "location": "Multiple hypermarkets"},
            {"name": "LuLu Hypermarket",      "url": "www.luluhypermarket.com",   "location": "Across UAE"},
            {"name": "iHerb",                 "url": "ae.iherb.com",             "location": "Online - ships to UAE"},
        ],
        "brands": [
            {"brand": "Centrum",      "product": "Adults Multivitamin",    "price_aed": "45-85"},
            {"brand": "Solgar",       "product": "Formula VM-75 Vitamins", "price_aed": "150-250"},
            {"brand": "Nature's Way", "product": "Alive! Multivitamin",    "price_aed": "90-160"},
        ],
    },

    "Omega-3 Fish Oil (EPA & DHA)": {
        "tip": "Very common in UAE pharmacies. Blackmores and Mollers are budget-friendly.",
        "stores": [
            {"name": "Life Pharmacy",         "url": "www.lifepharmacy.com",     "location": "500+ branches UAE"},
            {"name": "Boots UAE",             "url": "www.boots.ae",             "location": "Dubai, Abu Dhabi"},
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",  "location": "Dubai, Abu Dhabi"},
            {"name": "Carrefour UAE",         "url": "www.carrefouruae.com",      "location": "Multiple locations"},
            {"name": "iHerb",                 "url": "ae.iherb.com",             "location": "Online - ships to UAE"},
        ],
        "brands": [
            {"brand": "Mollers",    "product": "Norwegian Fish Oil",   "price_aed": "55-100"},
            {"brand": "Solgar",     "product": "Omega-3 950mg",        "price_aed": "130-220"},
            {"brand": "Blackmores", "product": "Omega Daily Fish Oil", "price_aed": "70-130"},
        ],
    },

    "Vitamin D3": {
        "tip": "Very affordable. Nature's Bounty is widely available and cheap across UAE.",
        "stores": [
            {"name": "Life Pharmacy",         "url": "www.lifepharmacy.com",     "location": "500+ branches UAE"},
            {"name": "Boots UAE",             "url": "www.boots.ae",             "location": "Dubai, Abu Dhabi"},
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",  "location": "Dubai, Abu Dhabi"},
            {"name": "Carrefour UAE",         "url": "www.carrefouruae.com",      "location": "Multiple locations"},
            {"name": "iHerb",                 "url": "ae.iherb.com",             "location": "Online - ships to UAE"},
        ],
        "brands": [
            {"brand": "Nature's Bounty", "product": "Vitamin D3 1000 IU", "price_aed": "25-55"},
            {"brand": "Solgar",          "product": "Vitamin D3 1000 IU", "price_aed": "80-140"},
        ],
    },

    "Caffeine (Pre-Workout)": {
        "tip": "Available at GNC stores in major UAE malls.",
        "stores": [
            {"name": "GNC UAE",       "url": "www.gnc.ae",                   "location": "Dubai Mall, Mall of Emirates"},
            {"name": "Amazon.ae",     "url": "www.amazon.ae/s?k=pre+workout", "location": "Online UAE delivery"},
            {"name": "Noon.com",      "url": "www.noon.com",                  "location": "Online UAE"},
            {"name": "MyProtein UAE", "url": "www.myprotein.com/ae",          "location": "Online - ships to UAE"},
        ],
        "brands": [
            {"brand": "Optimum Nutrition", "product": "Gold Standard Pre-Workout", "price_aed": "160-280"},
            {"brand": "MyProtein",         "product": "THE Pre-Workout",           "price_aed": "120-200"},
        ],
    },

    "BCAAs (Branched-Chain Amino Acids)": {
        "tip": "Scivation Xtend is the most popular BCAA brand in UAE gyms.",
        "stores": [
            {"name": "GNC UAE",   "url": "www.gnc.ae",               "location": "Major malls across UAE"},
            {"name": "Amazon.ae", "url": "www.amazon.ae/s?k=bcaa",   "location": "Online UAE delivery"},
            {"name": "iHerb",     "url": "ae.iherb.com",             "location": "Ships to UAE"},
            {"name": "Noon.com",  "url": "www.noon.com",             "location": "Online UAE"},
        ],
        "brands": [
            {"brand": "Scivation Xtend", "product": "BCAA Powder", "price_aed": "130-220"},
            {"brand": "MyProtein",       "product": "BCAA 2:1:1",  "price_aed": "80-150"},
        ],
    },

    "Magnesium (Glycinate or Citrate)": {
        "tip": "Holland & Barrett UAE stocks the best magnesium options.",
        "stores": [
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",      "location": "Dubai, Abu Dhabi"},
            {"name": "Life Pharmacy",         "url": "www.lifepharmacy.com",          "location": "500+ branches UAE"},
            {"name": "iHerb",                 "url": "ae.iherb.com",                 "location": "Ships to UAE"},
            {"name": "Amazon.ae",             "url": "www.amazon.ae/s?k=magnesium",  "location": "Online UAE delivery"},
        ],
        "brands": [
            {"brand": "Solgar",        "product": "Magnesium Citrate 200mg",   "price_aed": "90-160"},
            {"brand": "Nature's Best", "product": "Magnesium Glycinate 400mg", "price_aed": "70-130"},
        ],
    },

    "Fibre Supplement (Psyllium Husk)": {
        "tip": "Metamucil is available at almost every pharmacy in the UAE.",
        "stores": [
            {"name": "Life Pharmacy",         "url": "www.lifepharmacy.com",     "location": "500+ branches UAE"},
            {"name": "Boots UAE",             "url": "www.boots.ae",             "location": "Dubai, Abu Dhabi"},
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",  "location": "Dubai, Abu Dhabi"},
            {"name": "Carrefour UAE",         "url": "www.carrefouruae.com",      "location": "Multiple locations"},
            {"name": "iHerb",                 "url": "ae.iherb.com",             "location": "Ships to UAE"},
        ],
        "brands": [
            {"brand": "Metamucil", "product": "Psyllium Husk Powder", "price_aed": "45-90"},
            {"brand": "Now Foods", "product": "Psyllium Husk Powder", "price_aed": "55-100"},
        ],
    },

    "Plant-Based Protein (Pea / Soy)": {
        "tip": "Holland & Barrett UAE has the best range of plant-based proteins locally.",
        "stores": [
            {"name": "Holland & Barrett UAE", "url": "www.hollandandbarrett.ae",       "location": "Dubai, Abu Dhabi"},
            {"name": "MyProtein UAE",         "url": "www.myprotein.com/ae",           "location": "Online - ships to UAE"},
            {"name": "iHerb",                 "url": "ae.iherb.com",                  "location": "Ships to UAE"},
            {"name": "Amazon.ae",             "url": "www.amazon.ae/s?k=pea+protein", "location": "Online UAE delivery"},
        ],
        "brands": [
            {"brand": "MyProtein", "product": "Pea Protein Isolate",  "price_aed": "130-220"},
            {"brand": "Orgain",    "product": "Organic Plant Protein", "price_aed": "180-300"},
        ],
    },
}


def get_uae_info(supplement_name):
    """
    Looks up UAE market information for a supplement.
    Returns the dictionary of stores and brands, or None if not found.
    """
    return UAE_MARKET.get(supplement_name, None)
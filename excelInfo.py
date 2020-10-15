# Contains values facilitating export to excel
TAG_PREFIX_IDENTIFIER = "$CT_"
MAX_ARGS_AMOUNT = 13
SUPPORTED_LANGUAGES = ["de", "en"]
BATTLE_HEADERS = {
    "en": ["Battle ID", "Mode", "Rule", "Result", "Our Points", "Opponents Points", "Stage", "Date",
           "Start", "End", "Elapsed", "Team/Ranked Power", "Opponent Power", "Predicted Power"],
    "de": ["Kampf ID", "Modus", "Regeln", "Ergebnis", "Unsere Punkte", "Gegnerische Punkte", "Arena",
           "Datum", "Anfang", "Ende", "Länge", "Team/Rang Power", "Gegner Power", "Prognostizierte Power"]
}
PLAYER_HEADERS = {
    "en": ["K/A", "Kills", "Specials", "Deaths", "Weapon", "Turf Inked", "ID"],
    "de": ["E/A", "Erledigt", "Ultras", "Tote", "Waffen", "Gebiet Färbt", "ID"]
}
TOP_HEADERS_0 = {
    "en": ["Battle Stats"],
    "de": ["Kampfstatistiken"]
}
TOP_HEADERS_1 = {
    "en": "Player Stats",
    "de": "Spielerstatistiken"
}
PLAYER = {
    "en": "Player ",
    "de": "Spieler "
}
OPPONENT = {
    "en": "Opponent ",
    "de": "Gegner "
}
MODE = {
    "en": {
        "ranked solo": 'Ranked',
        "league pair": 'League Pair',
        "league team": 'League',
        "turf war": 'Turf War',
        "splatfest pro / solo": 'Splatfest Pro',
        "splatfest normal / team": 'Splatfest',
        "private": 'Private'
    },
    "de": {
        "ranked solo": 'Rang',
        "league pair": 'Liga 2er',
        "league team": 'Liga 4er',
        "turf war": 'Revierkampf',
        "splatfest pro / solo": 'Splatfest Pro',
        "splatfest normal / team": 'Splatfest',
        "private": 'Privat'
    }
}
RULE = {
    "en": {
        "tower_control": 'Tower Control',
        "splat_zones": 'Splat Zones',
        "rainmaker": 'Rainmaker',
        "clam_blitz": 'Clam Blitz',
        "turf_war": 'Turf War'
    },
    "de": {
        "tower_control": 'Turm Kommando',
        "splat_zones": 'Herrschaft',
        "rainmaker": 'Goldfisch',
        "clam_blitz": 'Muschel Chaos',
        "turf_war": 'Revierkampf'
    }
}
RESULT = {
    "en": {
        "defeat": 'Defeat',
        "victory": 'Victory'
    },
    "de": {
        "defeat": 'Verloren',
        "victory": 'Gewonnen'
    }
}
STAGE = {
    "en": {
        0: 'The Reef',
        1: 'Mussleforge Fitness',
        2: 'Starfish Mainstage',
        3: 'Sturgeon Shipyard',
        4: 'Inkblot Art Academy',
        5: 'Humpback Pump Track',
        6: 'Manta Maria',
        7: 'Port Mackerel',
        8: 'Moray Towers',
        9: 'Snapper Canal',
        10: 'Kelp Dome',
        11: 'Blackbelly Skatepark',
        12: 'Shellendorf Institute',
        13: 'MakoMart',
        14: 'Walleye Warehouse',
        15: 'Arowana Mall',
        16: 'Camp Triggerfish',
        17: 'Piranha Pit',
        18: 'Goby Arena',
        19: 'New Albacore Hotel',
        20: 'Wahoo World',
        21: 'Ancho-V Games',
        22: 'Skipper Pavilion',
        100: 'Shifty',
        101: 'Shifty: Wayslide',
        102: 'Shifty: S.P.L.A.T.',
        103: 'Shifty: Goosponge',
        105: 'Shifty: Windmill',
        106: 'Shifty: Spew',
        107: 'Shifty: Glass',
        108: 'Shifty: Cannon',
        109: 'Shifty: Bunker',
        110: 'Shifty: Grapplink',
        111: 'Shifty: Longshocking',
        112: 'Shifty: Balance',
        113: 'Shifty: Tentacles',
        114: 'Shifty: Switches',
        115: 'Shifty: Bouncey',
        116: 'Shifty: Railway',
        117: 'Shifty: Gusher',
        118: 'Shifty: Dasher',
        119: 'Shifty: Flooders',
        120: 'Shifty: Zones',
        121: 'Shifty: Spreading',
        122: 'Shifty: Tentaswitchia',
        123: 'Shifty: Rolonium',
        124: 'Shifty: Furler',
        9999: 'Shifty: Diaries'
    },
    "de": {
        0: 'Korallenviertel',  # The Reef
        1: 'Molluskelbude',  # Musselforge Fitness
        2: 'Seeigel-Rockbühne',  # Starfish Mainstage
        3: 'Störwerft',  # Sturgeon Shipyard
        4: 'Perlmutt-Akademie',  # Inkblot Art Academy
        5: 'Buckelwal-Piste',  # Humpback Pump Track
        6: 'Manta Mari',  # Manta Maria
        7: 'Heilbutt-Hafen',  # Port Mackerel
        8: 'Muränentürme',  # Moray Towers
        9: 'Grätenkanal',  # Snapper Canal
        10: 'Tümmlerkuppel',  # Kelp Dome
        11: 'Punkasius-Skatepark',  # Blackbelly Skatepark
        12: 'Abyssal-Museum',  # Shellendorf Institute
        13: 'Cetacea Market',  # MakoMart
        14: 'Kofferfisch-Lager',  # Walleye Warehouse
        15: 'Arowana Center',  # Arowana Mall
        16: 'Camp Schützenfisch',  # Camp Triggerfish
        17: 'Steinköhler-Grube',  # Piranha Pit
        18: 'Backfisch-Stadion',  # Goby Arena
        19: 'Hotel Neothun',  # New Albacore Hotel
        20: 'Flunder-Funpark',  # Wahoo World
        21: 'Anchobit Games HQ',  # Ancho-V Games
        22: 'Grundel-Pavillon',  # Skipper Pavilion
        100: 'Shifty: Windmill House on the Pearlie',  # Shifty: Windmill House on the Pearlie
        101: 'Shifty: Wayslide Cool',  # Shifty: Wayslide Cool
        102: 'Shifty: The Secret of S.P.L.A.T.',  # Shifty: The Secret of S.P.L.A.T.
        103: 'Shifty: Goosponge',  # Shifty: Goosponge
        105: 'Shifty: Cannon Fire Pearl',  # Shifty: Cannon Fire Pearl
        106: 'Shifty: Zone of Glass',  # Shifty: Zone of Glass
        107: 'Shifty: Fancy Spew',  # Shifty: Fancy Spew
        108: 'Shifty: Grapplink Girl',  # Shifty: Grapplink Girl
        109: 'Shifty: Zappy Longshocking',  # Shifty: Zappy Longshocking
        110: 'Shifty: The Bunker Games',  # Shifty: The Bunker Games
        111: 'hifty: A Swiftly Tilting Balance',  # Shifty: A Swiftly Tilting Balance
        112: 'Shifty: The Switches',  # Shifty: The Switches
        113: 'Shifty: Sweet Valley Tentacles',  # Shifty: Sweet Valley Tentacles
        114: 'Shifty: The Bouncey Twins',  # Shifty: The Bouncey Twins
        115: 'Shifty: Railway ChillinShifty',  # Shifty: Railway Chillin
        116: 'Shifty: Gusher Towns',  # Shifty: Gusher Towns
        117: 'Shifty: The Maze Dasher',  # Shifty: The Maze Dasher
        118: 'Shifty: Flooders in the Attic',  # Shifty: Flooders in the Attic
        119: 'Shifty: The Splat in Our Zones',  # Shifty: The Splat in Our Zones
        120: 'Shifty: The Ink is Spreading',  # Shifty: The Ink is Spreading
        121: 'Shifty: Bridge to Tentaswitchia',  # Shifty: Bridge to Tentaswitchia
        122: 'Shifty: The Chronicles of Rolonium',  # Shifty: The Chronicles of Rolonium
        123: 'Shifty: Furler in the Ashe',  # Shifty: Furler in the Ashes
        124: 'Shifty: MC.Princess Diaries',  # Shifty: MC.Princess Diaries
        9999: 'Shifty Station'  # Shifty Station
    }
}
WEAPONS = {
    "en": {
        0: 'Sploosh-o-matic',
        1: 'Neo Sploosh-o-matic',  # Neo Sploosh-o-matic
        2: 'Sploosh-o-matic 7',  # Sploosh-o-matic 7
        10: 'Splattershot Jr.',  # Splattershot Jr.
        11: 'Custom Splattershot Jr.',  # Custom Splattershot Jr.
        12: 'Kensa Splattershot Jr.',  # Kensa Splattershot Jr.
        20: 'Splash-o-matic',  # Splash-o-matic
        21: 'Neo Splash-o-matic',  # Neo Splash-o-matic
        30: 'Aerospray MG',  # Aerospray MG
        31: 'Aerospray RG',  # Aerospray RG
        32: 'Aerospray PG',  # Aerospray PG
        40: 'Splattershot',  # Splattershot
        41: 'Tentatek Splattershot',  # Tentatek Splattershot
        42: 'Kensa Splattershot',  # Kensa Splattershot
        45: 'Hero Shot Replica',  # Hero Shot Replica
        46: 'Octo Shot Replica',  # Octo Shot Replica
        50: '.52 Gal',  # .52 Gal
        51: '.52 Gal Deco',  # .52 Gal Deco
        52: 'Kensa .52 Gal',  # Kensa .52 Gal
        60: 'N-ZAP \'85',  # N-ZAP '85
        61: 'N-ZAP \'89',  # N-ZAP '89
        62: 'N-ZAP \'83',  # N-ZAP '83
        70: 'Splattershot Pro',  # Splattershot Pro
        71: 'Forge Splattershot Pro',  # Forge Splattershot Pro
        72: 'Kensa Splattershot Pro',  # Kensa Splattershot Pro
        80: '.96 Gal',  # .96 Gal
        81: '.96 Gal Deco',  # .96 Gal Deco
        90: 'Jet Squelcher',  # Jet Squelcher
        91: 'Custom Jet Squelcher',  # Custom Jet Squelcher
        200: 'Luna Blaster',  # Luna Blaster
        201: 'Luna Blaster Neo',  # Luna Blaster Neo
        202: 'Kensa Luna Blaster',  # Kensa Luna Blaster
        210: 'Blaster',  # Blaster
        211: 'Custom Blaster',  # Custom Blaster
        215: 'Hero Blaster Replica',  # Hero Blaster Replica
        220: 'Range Blaster',  # Range Blaster
        221: 'Custom Range Blaster',  # Custom Range Blaster
        222: 'Grim Range Blaster',  # Grim Range Blaster
        230: 'Clash Blaster',  # Clash Blaster
        231: 'Clash Blaster Neo',  # Clash Blaster Neo
        240: 'Rapid Blaster',  # Rapid Blaster
        241: 'Rapid Blaster Deco',  # Rapid Blaster Deco
        242: 'Kensa Rapid Blaster',  # Kensa Rapid Blaster
        250: 'Rapid Blaster Pro',  # Rapid Blaster Pro
        251: 'Rapid Blaster Pro Deco',  # Rapid Blaster Pro Deco
        300: 'L-3 Nozzlenose',  # L-3 Nozzlenose
        301: 'L-3 Nozzlenose D',  # L-3 Nozzlenose D
        302: 'Kensa L-3 Nozzlenose',  # Kensa L-3 Nozzlenose
        310: 'H-3 Nozzlenose',  # H-3 Nozzlenose
        311: 'H-3 Nozzlenose D',  # H-3 Nozzlenose D
        312: 'Cherry H-3 Nozzlenose',  # Cherry H-3 Nozzlenose
        400: 'Squeezer',  # Squeezer
        401: 'Foil Squeezer',  # Foil Squeezer
        1000: 'Carbon Roller',  # Carbon Roller
        1001: 'Carbon Roller Deco',  # Carbon Roller Deco
        1010: 'Splat Roller',  # Splat Roller
        1011: 'Krak-On Splat Roller',  # Krak-On Splat Roller
        1012: 'Kensa Splat Roller',  # Kensa Splat Roller
        1015: 'Hero Roller Replica',  # Hero Roller Replica
        1020: 'Dynamo Roller',  # Dynamo Roller
        1021: 'Gold Dynamo Roller',  # Gold Dynamo Roller
        1022: 'Kensa Dynamo Roller',  # Kensa Dynamo Roller
        1030: 'Flingza Roller',  # Flingza Roller
        1031: 'Foil Flingza Roller',  # Foil Flingza Roller
        1100: 'Inkbrush',  # Inkbrush
        1101: 'Inkbrush Nouveau',  # Inkbrush Nouveau
        1102: 'Permanent Inkbrush',  # Permanent Inkbrush
        1110: 'Octobrush',  # Octobrush
        1111: 'Octobrush Nouveau',  # Octobrush Nouveau
        1112: 'Kensa Octobrush',  # Kensa Octobrush
        1115: 'Herobrush Replica',  # Herobrush Replica
        2000: 'Classic Squiffer',  # Classic Squiffer
        2001: 'New Squiffer',  # New Squiffer
        2002: 'Fresh Squiffer',  # Fresh Squiffer
        2010: 'Splat Charger',  # Splat Charger
        2011: 'Firefin Splat Charger',  # Firefin Splat Charger
        2012: 'Kensa Charger',  # Kensa Charger
        2015: 'Hero Charger Replica',  # Hero Charger Replica
        2020: 'Splatterscope',  # Splatterscope
        2021: 'Firefin Splatterscope',  # Firefin Splatterscope
        2022: 'Kensa Splatterscope',  # Kensa Splatterscope
        2030: 'E-liter 4K',  # E-liter 4K
        2031: 'Custom E-liter 4K',  # Custom E-liter 4K
        2040: 'E-liter 4K Scope',  # E-liter 4K Scope
        2041: 'Custom E-liter 4K Scope',  # Custom E-liter 4K Scope
        2050: 'Bamboozler 14 Mk I',  # Bamboozler 14 Mk I
        2051: 'Bamboozler 14 Mk II',  # Bamboozler 14 Mk II
        2052: 'Bamboozler 14 Mk III',  # Bamboozler 14 Mk III
        2060: 'Goo Tuber',  # Goo Tuber
        2061: 'Custom Goo Tuber',  # Custom Goo Tuber
        3000: 'Slosher',  # Slosher
        3001: 'Slosher Deco',  # Slosher Deco
        3002: 'Soda Slosher',  # Soda Slosher
        3005: 'Hero Slosher Replica',  # Hero Slosher Replica
        3010: 'Tri-Slosher',  # Tri-Slosher
        3011: 'Tri-Slosher Nouveau',  # Tri-Slosher Nouveau
        3020: 'Sloshing Machine',  # Sloshing Machine
        3021: 'Sloshing Machine Neo',  # Sloshing Machine Neo
        3022: 'Kensa Sloshing Machine',  # Kensa Sloshing Machine
        3030: 'Bloblobber',  # Bloblobber
        3031: 'Bloblobber Deco',  # Bloblobber Deco
        3040: 'Explosher',  # Explosher
        3041: 'Custom Explosher',  # Custom Explosher
        4000: 'Mini Splatling',  # Mini Splatling
        4001: 'Zink Mini Splatling',  # Zink Mini Splatling
        4002: 'Kensa Mini Splatling',  # Kensa Mini Splatling
        4010: 'Heavy Splatling',  # Heavy Splatling
        4011: 'Heavy Splatling Deco',  # Heavy Splatling Deco
        4012: 'Heavy Splatling Remix',  # Heavy Splatling Remix
        4015: 'Hero Splatling Replica',  # Hero Splatling Replica
        4020: 'Hydra Splatling',  # Hydra Splatling
        4021: 'Custom Hydra Splatling',  # Custom Hydra Splatling
        4030: 'Ballpoint Splatling',  # Ballpoint Splatling
        4031: 'Ballpoint Splatling Nouveau',  # Ballpoint Splatling Nouveau
        4040: 'Nautilus 47',  # Nautilus 47
        4041: 'Nautilus 79',  # Nautilus 79
        5000: 'Dapple Dualies',  # Dapple Dualies
        5001: 'Dapple Dualies Nouveau',  # Dapple Dualies Nouveau
        5002: 'Clear Dapple Dualies',  # Clear Dapple Dualies
        5010: 'Splat Dualies',  # Splat Dualies
        5011: 'Enperry Splat Dualies',  # Enperry Splat Dualies
        5012: 'Kensa Splat Dualies',  # Kensa Splat Dualies
        5015: 'Hero Dualie Replicas',  # Hero Dualie Replicas
        5020: 'Glooga Dualies',  # Glooga Dualies
        5021: 'Glooga Dualies Deco',  # Glooga Dualies Deco
        5022: 'Kensa Glooga Dualies',  # Kensa Glooga Dualies
        5030: 'Dualie Squelchers',  # Dualie Squelchers
        5031: 'Custom Dualie Squelchers',  # Custom Dualie Squelchers
        5040: 'Dark Tetra Dualies',  # Dark Tetra Dualies
        5041: 'Light Tetra Dualies',  # Light Tetra Dualies
        6000: 'Splat Brella',  # Splat Brella
        6001: 'Sorella Brella',  # Sorella Brella
        6005: 'Hero Brella Replica',  # Hero Brella Replica
        6010: 'Tenta Brella',  # Tenta Brella
        6011: 'Tenta Sorella Brella',  # Tenta Sorella Brella
        6012: 'Tenta Camo Brella',  # Tenta Camo Brella
        6020: 'Undercover Brella',  # Undercover Brella
        6021: 'Undercover Sorella Brella',  # Undercover Sorella Brella
        6022: 'Kensa Undercover Brella',  # Kensa Undercover Brella
        20000: 'Grizzco Blaster',  # Grizzco Blaster
        20010: 'Grizzco Brella',  # Grizzco Brella
        20020: 'Grizzco Charger',  # Grizzco Charger
        20030: 'Grizzco Slosher'  # Grizzco Slosher
    },
    "de": {
        0: 'Disperser',
        1: 'Disperser Neo',  # Neo Sploosh-o-matic
        2: 'Disperser 7',  # Sploosh-o-matic 7
        10: 'Junior-Kleckser',  # Splattershot Jr.
        11: 'Junior-Kleckser Plus',  # Custom Splattershot Jr.
        12: 'Kensa-Junior-Kleckser',  # Kensa Splattershot Jr.
        20: 'Fein-Disperser',  # Splash-o-matic
        21: 'Fein-Disperser Neo',  # Neo Splash-o-matic
        30: 'Airbrush MG',  # Aerospray MG
        31: 'Airbrush RG',  # Aerospray RG
        32: 'Airbrush PG',  # Aerospray PG
        40: 'Kleckser',  # Splattershot
        41: 'Tentatek-Kleckser',  # Tentatek Splattershot
        42: 'Kensa-Kleckser',  # Kensa Splattershot
        45: 'Heldenwaffe Replik',  # Hero Shot Replica
        46: 'Oktowaffe Replik',  # Octo Shot Replica
        50: '.52 Gallon',  # .52 Gal
        51: '.52 Gallon Deko',  # .52 Gal Deco
        52: 'Kensa-.52 Gallon',  # Kensa .52 Gal
        60: 'N-ZAP85',  # N-ZAP '85
        61: 'N-ZAP89',  # N-ZAP '89
        62: 'N-ZAP83',  # N-ZAP '83
        70: 'Profi-Kleckser',  # Splattershot Pro
        71: 'Focus-Profi-Kleckser',  # Forge Splattershot Pro
        72: 'Kensa-Profi-Kleckser',  # Kensa Splattershot Pro
        80: '.96 Gallon',  # .96 Gal
        81: '.96 Gallon Deko',  # .96 Gal Deco
        90: 'Platscher',  # Jet Squelcher
        91: 'Platscher SE',  # Custom Jet Squelcher
        200: 'Luna-Blaster',  # Luna Blaster
        201: 'Luna-Blaster Neo',  # Luna Blaster Neo
        202: 'Kensa-Luna-Blaster',  # Kensa Luna Blaster
        210: 'Blaster',  # Blaster
        211: 'Blaster SE',  # Custom Blaster
        215: 'Helden-Blaster Replik',  # Hero Blaster Replica
        220: 'Fern-Blaster',  # Range Blaster
        221: 'Fern-Blaster SE',  # Custom Range Blaster
        222: 'Fern-Blaster Inferno',  # Grim Range Blaster
        230: 'Kontra-Blaster',  # Clash Blaster
        231: 'Kontra-Blaster Neo',  # Clash Blaster Neo
        240: 'Turbo-Blaster',  # Rapid Blaster
        241: 'Turbo-Blaster Deko',  # Rapid Blaster Deco
        242: 'Kensa-Turbo-Blaster',  # Kensa Rapid Blaster
        250: 'Turbo-Blaster Plus',  # Rapid Blaster Pro
        251: 'Turbo-Blaster Plus Deko',  # Rapid Blaster Pro Deco
        300: 'L3 Tintenwerfer',  # L-3 Nozzlenose
        301: 'L3 Tintenwerfer D',  # L-3 Nozzlenose D
        302: 'Kensa-L3 Tintenwerfer',  # Kensa L-3 Nozzlenose
        310: 'S3 Tintenwerfer',  # H-3 Nozzlenose
        311: 'S3 Tintenwerfer D',  # H-3 Nozzlenose D
        312: 'S3 Tintenwerfer Kirsch',  # Cherry H-3 Nozzlenose
        400: 'Quetscher',  # Squeezer
        401: 'Quetscher Fol',  # Foil Squeezer
        1000: 'Karbonroller',  # Carbon Roller
        1001: 'Karbonroller Deko',  # Carbon Roller Deco
        1010: 'Klecksroller',  # Splat Roller
        1011: 'Medusa-Klecksroller',  # Krak-On Splat Roller
        1012: 'Kensa-Klecksroller',  # Kensa Splat Roller
        1015: 'Helden-Roller Replik',  # Hero Roller Replica
        1020: 'Dynaroller',  # Dynamo Roller
        1021: 'Dynaroller Tesla',  # Gold Dynamo Roller
        1022: 'Kensa-Dynaroller',  # Kensa Dynamo Roller
        1030: 'Flex-Roller',  # Flingza Roller
        1031: 'Flex-Roller Fol',  # Foil Flingza Roller
        1100: 'Quasto',  # Inkbrush
        1101: 'Quasto Fresco',  # Inkbrush Nouveau
        1102: 'Quasto Permanent',  # Permanent Inkbrush
        1110: 'Kalligraf',  # Octobrush
        1111: 'Kalligraf Fresco',  # Octobrush Nouveau
        1112: 'Kensa-Kalligraf',  # Kensa Octobrush
        1115: 'Helden-Pinsel Replik',  # Herobrush Replica
        2000: 'Sepiator α',  # Classic Squiffer
        2001: 'Sepiator β',  # New Squiffer
        2002: 'Sepiator γ',  # Fresh Squiffer
        2010: 'Klecks-Konzentrator',  # Splat Charger
        2011: 'Rilax-Klecks-Konzentrator',  # Firefin Splat Charger
        2012: 'Kensa-Klecks-Konzentrator',  # Kensa Charger
        2015: 'Helden-Konzentrator Replik',  # Hero Charger Replica
        2020: 'Ziel-Konzentrator',  # Splatterscope
        2021: 'Rilax-Ziel-Konzentrator',  # Firefin Splatterscope
        2022: 'Kensa-Ziel-Konzentrator',  # Kensa Splatterscope
        2030: 'E-liter 4K',  # E-liter 4K
        2031: 'E-liter 4K SE',  # Custom E-liter 4K
        2040: 'Ziel-E-liter 4K',  # E-liter 4K Scope
        2041: 'Ziel-E-liter 4K SE',  # Custom E-liter 4K Scope
        2050: 'Klotzer 14-A',  # Bamboozler 14 Mk I
        2051: 'Klotzer 14-B',  # Bamboozler 14 Mk II
        2052: 'Klotzer 14-C',  # Bamboozler 14 Mk III
        2060: 'T-Tuber',  # Goo Tuber
        2061: 'T-Tuber SE',  # Custom Goo Tuber
        3000: 'Schwapper',  # Slosher
        3001: 'Schwapper Deko',  # Slosher Deco
        3002: 'Sprudel-Schwapper',  # Soda Slosher
        3005: 'Helden-Schwapper Replik',  # Hero Slosher Replica
        3010: '3R-Schwapper',  # Tri-Slosher
        3011: '3R-Schwapper Fresco',  # Tri-Slosher Nouveau
        3020: 'Trommel-Schwapper',  # Sloshing Machine
        3021: 'Trommel-Schwapper Neo',  # Sloshing Machine Neo
        3022: 'Kensa-Trommel-Schwapper',  # Kensa Sloshing Machine
        3030: 'Wannen-Schwapper',  # Bloblobber
        3031: 'Wannen-Schwapper Deko',  # Bloblobber Deco
        3040: 'Knall-Schwapper',  # Explosher
        3041: 'Knall-Schwapper SE',  # Custom Explosher
        4000: 'Klecks-Splatling',  # Mini Splatling
        4001: 'Sagitron-Klecks-Splatling',  # Zink Mini Splatling
        4002: 'Kensa-Klecks-Splatling',  # Kensa Mini Splatling
        4010: 'Splatling',  # Heavy Splatling
        4011: 'Splatling Deko',  # Heavy Splatling Deco
        4012: 'Splatling Ultrabass',  # Heavy Splatling Remix
        4015: 'Helden-Splatling Replik',  # Hero Splatling Replica
        4020: 'Hydrant',  # Hydra Splatling
        4021: 'Hydrant SE',  # Custom Hydra Splatling
        4030: 'Kuli-Splatling',  # Ballpoint Splatling
        4031: 'Kuli-Splatling Fresco',  # Ballpoint Splatling Nouveau
        4040: 'Nautilus 47',  # Nautilus 47
        4041: 'Nautilus 79',  # Nautilus 79
        5000: 'Sprenkler',  # Dapple Dualies
        5001: 'Sprenkler Fresco',  # Dapple Dualies Nouveau
        5002: 'Hell Sprenkler',  # Clear Dapple Dualies
        5010: 'Klecks-Doppler',  # Splat Dualies
        5011: 'Enperry-Klecks-Doppler',  # Enperry Splat Dualies
        5012: 'Kensa-Klecks-Doppler',  # Kensa Splat Dualies
        5015: 'Helden-Doppler Replik',  # Hero Dualie Replicas
        5020: 'Kelvin 525',  # Glooga Dualies
        5021: 'Kelvin 525 Deko',  # Glooga Dualies Deco
        5022: 'Kensa-Kelvin-525',  # Kensa Glooga Dualies
        5030: 'Dual-Platscher',  # Dualie Squelchers
        5031: 'Dual-Platscher SE',  # Custom Dualie Squelchers
        5040: 'Quadhopper Noir',  # Dark Tetra Dualies
        5041: 'Quadhopper Blanc',  # Light Tetra Dualies
        6000: 'Parapluviator',  # Splat Brella
        6001: 'Sorella-Parapluviator',  # Sorella Brella
        6005: 'Helden-Pluviator Replik',  # Hero Brella Replica
        6010: 'Camp-Pluviator',  # Tenta Brella
        6011: 'Sorella-Camp-Pluviator',  # Tenta Sorella Brella
        6012: 'Camp-Pluviator-Camo',  # Tenta Camo Brella
        6020: 'UnderCover',  # Undercover Brella
        6021: 'Sorella-UnderCover',  # Undercover Sorella Brella
        6022: 'Kensa-UnderCover',  # Kensa Undercover Brella
        20000: 'Grizzco Blaster',  # Grizzco Blaster
        20010: 'Grizzco Brella',  # Grizzco Brella
        20020: 'Grizzco Charger',  # Grizzco Charger
        20030: 'Grizzco Slosher'  # Grizzco Slosher
    }
}

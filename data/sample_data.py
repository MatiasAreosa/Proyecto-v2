"""
Datos de muestra realistas para el Agente IA Aeronáutico.
Incluye aeropuertos, aerolíneas, reservas, PNRs y tarifas.
"""

AIRPORTS = {
    "GRU": {"city": "São Paulo",      "country": "Brasil",        "name": "Guarulhos International",         "zone": "LAC"},
    "GIG": {"city": "Río de Janeiro", "country": "Brasil",        "name": "Galeão International",            "zone": "LAC"},
    "EZE": {"city": "Buenos Aires",   "country": "Argentina",     "name": "Ministro Pistarini",              "zone": "LAC"},
    "AEP": {"city": "Buenos Aires",   "country": "Argentina",     "name": "Jorge Newbery",                   "zone": "LAC"},
    "SCL": {"city": "Santiago",       "country": "Chile",         "name": "Arturo Merino Benítez",           "zone": "LAC"},
    "BOG": {"city": "Bogotá",         "country": "Colombia",      "name": "El Dorado International",         "zone": "LAC"},
    "MDE": {"city": "Medellín",       "country": "Colombia",      "name": "José María Córdova",              "zone": "LAC"},
    "LIM": {"city": "Lima",           "country": "Perú",          "name": "Jorge Chávez International",      "zone": "LAC"},
    "UIO": {"city": "Quito",          "country": "Ecuador",       "name": "Mariscal Sucre International",    "zone": "LAC"},
    "PTY": {"city": "Panamá",         "country": "Panamá",        "name": "Tocumen International",           "zone": "LAC"},
    "MIA": {"city": "Miami",          "country": "EE.UU.",        "name": "Miami International",             "zone": "NAM"},
    "JFK": {"city": "Nueva York",     "country": "EE.UU.",        "name": "John F. Kennedy International",   "zone": "NAM"},
    "LAX": {"city": "Los Ángeles",    "country": "EE.UU.",        "name": "Los Angeles International",       "zone": "NAM"},
    "ORD": {"city": "Chicago",        "country": "EE.UU.",        "name": "O'Hare International",            "zone": "NAM"},
    "MAD": {"city": "Madrid",         "country": "España",        "name": "Adolfo Suárez Madrid-Barajas",    "zone": "EUR"},
    "LHR": {"city": "Londres",        "country": "Reino Unido",   "name": "Heathrow Airport",                "zone": "EUR"},
    "CDG": {"city": "París",          "country": "Francia",       "name": "Charles de Gaulle",               "zone": "EUR"},
    "FRA": {"city": "Frankfurt",      "country": "Alemania",      "name": "Frankfurt am Main",               "zone": "EUR"},
    "AMS": {"city": "Ámsterdam",      "country": "P. Bajos",      "name": "Amsterdam Schiphol",              "zone": "EUR"},
    "BCN": {"city": "Barcelona",      "country": "España",        "name": "Josep Tarradellas Barcelona-El Prat", "zone": "EUR"},
    "MEX": {"city": "Cdad. México",   "country": "México",        "name": "Benito Juárez International",     "zone": "NAM"},
    "CUN": {"city": "Cancún",         "country": "México",        "name": "Cancún International",            "zone": "NAM"},
    "MVD": {"city": "Montevideo",     "country": "Uruguay",       "name": "Carrasco International",          "zone": "LAC"},
    "ASU": {"city": "Asunción",       "country": "Paraguay",      "name": "Silvio Pettirossi International", "zone": "LAC"},
    "CCS": {"city": "Caracas",        "country": "Venezuela",     "name": "Simón Bolívar International",     "zone": "LAC"},
}

AIRLINES = {
    "LA": {"name": "LATAM Airlines",         "country": "Chile",      "iata": "LA", "icao": "LAN", "alliance": "oneworld"},
    "AA": {"name": "American Airlines",       "country": "EE.UU.",     "iata": "AA", "icao": "AAL", "alliance": "oneworld"},
    "IB": {"name": "Iberia",                  "country": "España",     "iata": "IB", "icao": "IBE", "alliance": "oneworld"},
    "BA": {"name": "British Airways",         "country": "RU",         "iata": "BA", "icao": "BAW", "alliance": "oneworld"},
    "AF": {"name": "Air France",              "country": "Francia",    "iata": "AF", "icao": "AFR", "alliance": "SkyTeam"},
    "LH": {"name": "Lufthansa",               "country": "Alemania",   "iata": "LH", "icao": "DLH", "alliance": "Star Alliance"},
    "CM": {"name": "Copa Airlines",           "country": "Panamá",     "iata": "CM", "icao": "CMP", "alliance": "Star Alliance"},
    "AV": {"name": "Avianca",                 "country": "Colombia",   "iata": "AV", "icao": "AVA", "alliance": "Star Alliance"},
    "AR": {"name": "Aerolíneas Argentinas",   "country": "Argentina",  "iata": "AR", "icao": "ARG", "alliance": "SkyTeam"},
    "G3": {"name": "Gol Transportes Aéreos",  "country": "Brasil",     "iata": "G3", "icao": "GLO", "alliance": "None"},
    "AD": {"name": "Azul Brazilian Airlines", "country": "Brasil",     "iata": "AD", "icao": "AZU", "alliance": "None"},
    "JJ": {"name": "LATAM Brasil",            "country": "Brasil",     "iata": "JJ", "icao": "TAM", "alliance": "oneworld"},
    "KL": {"name": "KLM",                     "country": "P. Bajos",   "iata": "KL", "icao": "KLM", "alliance": "SkyTeam"},
    "UA": {"name": "United Airlines",         "country": "EE.UU.",     "iata": "UA", "icao": "UAL", "alliance": "Star Alliance"},
    "DL": {"name": "Delta Air Lines",         "country": "EE.UU.",     "iata": "DL", "icao": "DAL", "alliance": "SkyTeam"},
}

# Tarifas por ruta en USD (adulto, ida)
ROUTE_FARES = {
    "EZE-MAD": {"F": 8500, "C": 4200, "W": 1800, "Y": 950,  "M": 680,  "K": 520,  "V": 380,  "N": 280},
    "EZE-MIA": {"F": 6800, "C": 3100, "W": 1200, "Y": 720,  "M": 490,  "K": 380,  "V": 260,  "N": 195},
    "EZE-JFK": {"F": 7200, "C": 3400, "W": 1350, "Y": 800,  "M": 560,  "K": 420,  "V": 295,  "N": 210},
    "EZE-SCL": {"F": 2800, "C": 1400, "W": 580,  "Y": 320,  "M": 220,  "K": 170,  "V": 130,  "N": 98},
    "EZE-GRU": {"F": 3200, "C": 1600, "W": 680,  "Y": 380,  "M": 260,  "K": 200,  "V": 150,  "N": 110},
    "GRU-MIA": {"F": 7500, "C": 3800, "W": 1500, "Y": 860,  "M": 620,  "K": 480,  "V": 340,  "N": 240},
    "GRU-JFK": {"F": 8000, "C": 4000, "W": 1600, "Y": 920,  "M": 660,  "K": 510,  "V": 365,  "N": 258},
    "GRU-MAD": {"F": 9000, "C": 4500, "W": 1900, "Y": 1050, "M": 750,  "K": 580,  "V": 415,  "N": 295},
    "GRU-LHR": {"F": 9500, "C": 4800, "W": 2000, "Y": 1100, "M": 790,  "K": 610,  "V": 435,  "N": 308},
    "SCL-MAD": {"F": 8200, "C": 4100, "W": 1750, "Y": 990,  "M": 710,  "K": 548,  "V": 392,  "N": 278},
    "SCL-MIA": {"F": 6500, "C": 3200, "W": 1300, "Y": 740,  "M": 530,  "K": 410,  "V": 292,  "N": 207},
    "BOG-MIA": {"F": 5800, "C": 2900, "W": 1100, "Y": 620,  "M": 445,  "K": 344,  "V": 245,  "N": 174},
    "BOG-MAD": {"F": 7800, "C": 3900, "W": 1650, "Y": 940,  "M": 675,  "K": 521,  "V": 372,  "N": 264},
    "LIM-MIA": {"F": 5600, "C": 2800, "W": 1050, "Y": 590,  "M": 424,  "K": 327,  "V": 233,  "N": 165},
    "LIM-MAD": {"F": 7600, "C": 3800, "W": 1600, "Y": 910,  "M": 653,  "K": 504,  "V": 360,  "N": 255},
    "PTY-MIA": {"F": 3500, "C": 1750, "W": 720,  "Y": 410,  "M": 295,  "K": 228,  "V": 163,  "N": 115},
    "MEX-MAD": {"F": 7200, "C": 3600, "W": 1520, "Y": 870,  "M": 625,  "K": 483,  "V": 345,  "N": 245},
    "MEX-MIA": {"F": 4200, "C": 2100, "W": 880,  "Y": 498,  "M": 358,  "K": 277,  "V": 198,  "N": 140},
}

CABIN_NAMES = {
    "F": "Primera Clase",
    "C": "Business/Ejecutiva",
    "W": "Premium Economy",
    "Y": "Economy (Full)",
    "M": "Economy (Flexible)",
    "K": "Economy (Standard)",
    "V": "Economy (Descuento)",
    "N": "Economy (Promocional)",
}

# Bases tarifarias con reglas
FARE_BASIS = {
    "YCA": {
        "class": "Y", "cabin": "Y", "name": "Economy Full",
        "refundable": True, "changeable": True,
        "advance_purchase": 0, "min_stay": None, "max_stay": "12M",
        "baggage": "2PC 23kg", "description": "Tarifa economy sin restricciones"
    },
    "MLAOAP3M": {
        "class": "M", "cabin": "Y", "name": "Economy Flexible",
        "refundable": True, "changeable": True, "change_fee": 150,
        "advance_purchase": 7, "min_stay": None, "max_stay": "3M",
        "baggage": "1PC 23kg", "description": "Economy con penalidad de cambio"
    },
    "KLAOAP14": {
        "class": "K", "cabin": "Y", "name": "Economy Standard",
        "refundable": False, "changeable": True, "change_fee": 200,
        "advance_purchase": 14, "min_stay": "7D", "max_stay": "1M",
        "baggage": "1PC 23kg", "description": "Compra anticipada 14 días, no reembolsable"
    },
    "VLAOAP21NR": {
        "class": "V", "cabin": "Y", "name": "Economy Descuento",
        "refundable": False, "changeable": False,
        "advance_purchase": 21, "min_stay": "7D", "max_stay": "1M",
        "baggage": "1PC 23kg", "description": "No reembolsable ni endosable, compra 21 días"
    },
    "NLAOSAPROMO": {
        "class": "N", "cabin": "Y", "name": "Economy Promo",
        "refundable": False, "changeable": False,
        "advance_purchase": 30, "min_stay": "14D", "max_stay": "14D",
        "baggage": "0PC (hand carry only)", "description": "Tarifa promocional, máximas restricciones"
    },
    "CCA": {
        "class": "C", "cabin": "C", "name": "Business Full",
        "refundable": True, "changeable": True,
        "advance_purchase": 0, "min_stay": None, "max_stay": "12M",
        "baggage": "2PC 32kg + carry-on", "description": "Business sin restricciones"
    },
    "CLA7AP": {
        "class": "C", "cabin": "C", "name": "Business Advance",
        "refundable": True, "changeable": True, "change_fee": 300,
        "advance_purchase": 7, "min_stay": None, "max_stay": "12M",
        "baggage": "2PC 32kg + carry-on", "description": "Business con compra anticipada"
    },
    "FCA": {
        "class": "F", "cabin": "F", "name": "Primera Clase",
        "refundable": True, "changeable": True,
        "advance_purchase": 0, "min_stay": None, "max_stay": "12M",
        "baggage": "3PC 32kg + carry-on", "description": "Primera clase sin restricciones"
    },
}

# PNRs de muestra
SAMPLE_PNRS = {
    "ABC123": {
        "localizador": "ABC123",
        "estado": "Confirmado",
        "fecha_creacion": "10ENE25",
        "agente": "BUEAA12AB",
        "pasajeros": [
            {"tipo": "ADT", "apellido": "GARCIA", "nombre": "CARLOS", "titulo": "MR", "fqtv": "LA-12345678"},
            {"tipo": "ADT", "apellido": "GARCIA", "nombre": "ANA", "titulo": "MRS"},
        ],
        "segmentos": [
            {
                "num": 1, "vuelo": "LA621", "clase": "Y", "status": "HK",
                "origen": "EZE", "destino": "GRU",
                "fecha": "15FEB25", "hora_salida": "0815", "hora_llegada": "1005",
                "equipo": "Boeing 787-9", "duracion": "1:50",
            },
            {
                "num": 2, "vuelo": "LA704", "clase": "Y", "status": "HK",
                "origen": "GRU", "destino": "MAD",
                "fecha": "15FEB25", "hora_salida": "2145", "hora_llegada": "1355+1",
                "equipo": "Boeing 777-300ER", "duracion": "10:10",
            },
        ],
        "contacto": {"telefono": "54115550000", "email": "cgarcia@email.com"},
        "ticketing": {"limite": "12FEB25/2359", "forma": "TAW"},
        "base_tarifa": "YLAOAP7",
        "tarifa_total": {"ADT": 1320.00, "tasas": 210.50, "total": 1530.50},
        "ssr": ["VGML-P1"],
    },
    "XYZ789": {
        "localizador": "XYZ789",
        "estado": "Emitido",
        "fecha_creacion": "03ENE25",
        "agente": "MIAAA08CD",
        "pasajeros": [
            {"tipo": "ADT", "apellido": "RODRIGUEZ", "nombre": "MARIA", "titulo": "MS"},
        ],
        "segmentos": [
            {
                "num": 1, "vuelo": "AA902", "clase": "C", "status": "HK",
                "origen": "MIA", "destino": "EZE",
                "fecha": "20ENE25", "hora_salida": "2355", "hora_llegada": "1325+1",
                "equipo": "Boeing 777-200", "duracion": "9:30",
            },
            {
                "num": 2, "vuelo": "AA903", "clase": "C", "status": "HK",
                "origen": "EZE", "destino": "MIA",
                "fecha": "27ENE25", "hora_salida": "2305", "hora_llegada": "0825+1",
                "equipo": "Boeing 777-200", "duracion": "8:20",
            },
        ],
        "contacto": {"telefono": "13055550000", "email": "mrodriguez@company.com"},
        "ticketing": {"limite": "Emitido", "numero_boleto": "0012341234567"},
        "base_tarifa": "CCA",
        "tarifa_total": {"ADT": 3400.00, "tasas": 285.00, "total": 3685.00},
        "ssr": [],
    },
    "DEF456": {
        "localizador": "DEF456",
        "estado": "En espera (WL)",
        "fecha_creacion": "15ENE25",
        "agente": "SCLLA02EF",
        "pasajeros": [
            {"tipo": "ADT", "apellido": "PEREZ", "nombre": "JUAN", "titulo": "MR"},
            {"tipo": "CNN", "apellido": "PEREZ", "nombre": "SOFIA", "titulo": "MISS"},
        ],
        "segmentos": [
            {
                "num": 1, "vuelo": "LA800", "clase": "Y", "status": "HL",
                "origen": "SCL", "destino": "MIA",
                "fecha": "28MAR25", "hora_salida": "1630", "hora_llegada": "2310",
                "equipo": "Airbus A321XLR", "duracion": "8:40",
            },
        ],
        "contacto": {"telefono": "56225550000"},
        "ticketing": {"limite": "20ENE25/1800"},
        "base_tarifa": "KLAOAP14",
        "tarifa_total": {"ADT": 740.00, "CNN": 518.00, "tasas": 195.00, "total": 1453.00},
        "ssr": ["UMNR-P2"],
    },
}

# Reservas mensuales (datos para reportes)
import random
random.seed(42)

ROUTES_POOL = [
    "EZE-MAD", "EZE-MIA", "EZE-JFK", "EZE-GRU", "EZE-SCL",
    "GRU-MIA", "GRU-MAD", "GRU-JFK", "SCL-MIA", "SCL-MAD",
    "BOG-MIA", "LIM-MIA", "PTY-MIA", "MEX-MAD",
]
AIRLINES_POOL = ["LA", "AA", "IB", "AF", "LH", "CM", "AV", "AR"]
CABINS_POOL   = list(CABIN_NAMES.keys())
CABIN_WEIGHTS = [1, 3, 4, 15, 20, 25, 20, 12]  # distribución realista

def _random_booking(month: int, year: int, idx: int) -> dict:
    route  = random.choice(ROUTES_POOL)
    cabin  = random.choices(CABINS_POOL, weights=CABIN_WEIGHTS, k=1)[0]
    origin, destination = route.split("-")
    base   = ROUTE_FARES.get(route, {}).get(cabin, 500)
    # pequeña variación de precio
    factor = random.uniform(0.85, 1.15)
    fare   = round(base * factor, 2)
    taxes  = round(fare * random.uniform(0.12, 0.22), 2)
    pax    = random.randint(1, 4)
    day    = random.randint(1, 28)
    airline = random.choice(AIRLINES_POOL)
    lf     = random.uniform(0.55, 0.98)
    seats  = random.choice([150, 180, 210, 250, 300, 350])
    return {
        "id": f"BK{year}{month:02d}{idx:04d}",
        "fecha_reserva": f"{day:02d}/{month:02d}/{year}",
        "mes": month, "anio": year,
        "ruta": route, "origen": origin, "destino": destination,
        "aerolinea": airline,
        "cabina": cabin,
        "clase": cabin,
        "tarifa_base": fare,
        "tasas": taxes,
        "total_pax": pax,
        "revenue": round((fare + taxes) * pax, 2),
        "load_factor": round(lf * 100, 1),
        "asientos_avion": seats,
        "km_vuelo": random.randint(500, 12000),
        "estado": random.choices(
            ["Confirmado", "Emitido", "Cancelado"],
            weights=[25, 65, 10], k=1
        )[0],
    }

SAMPLE_BOOKINGS: list[dict] = []
for yr in [2024, 2025]:
    for mo in range(1, 13):
        count = random.randint(180, 320)
        for i in range(count):
            SAMPLE_BOOKINGS.append(_random_booking(mo, yr, i + 1))


def get_bookings(mes: int | None = None, anio: int | None = None,
                 ruta: str | None = None, cabina: str | None = None,
                 estado: str | None = None) -> list[dict]:
    """Filtra reservas según los criterios dados."""
    result = SAMPLE_BOOKINGS
    if mes:
        result = [b for b in result if b["mes"] == mes]
    if anio:
        result = [b for b in result if b["anio"] == anio]
    if ruta:
        result = [b for b in result if ruta.upper() in b["ruta"]]
    if cabina:
        result = [b for b in result if b["cabina"] == cabina.upper()]
    if estado:
        result = [b for b in result if b["estado"].lower() == estado.lower()]
    return result


# Disponibilidad simulada
AVAILABILITY_TEMPLATE = {
    "EZE-MAD": [
        {"flight": "IB6841", "dep": "13:45", "arr": "06:30+1", "stops": 0, "equip": "A350-900",
         "seats": {"F": 4, "C": 18, "W": 24, "Y": 42, "M": 28, "K": 15, "V": 8, "N": 3}},
        {"flight": "LA705",  "dep": "22:15", "arr": "14:55+1", "stops": 0, "equip": "B787-9",
         "seats": {"F": 2, "C": 30, "W": 0,  "Y": 55, "M": 40, "K": 22, "V": 12, "N": 5}},
    ],
    "EZE-MIA": [
        {"flight": "AA900",  "dep": "23:55", "arr": "08:25+1", "stops": 0, "equip": "B777-200",
         "seats": {"F": 0, "C": 12, "W": 0,  "Y": 60, "M": 45, "K": 30, "V": 18, "N": 9}},
        {"flight": "LA551",  "dep": "09:30", "arr": "17:10",   "stops": 1, "equip": "B767-300",
         "seats": {"F": 0, "C": 8,  "W": 0,  "Y": 38, "M": 25, "K": 14, "V": 6,  "N": 2}},
    ],
    "GRU-MAD": [
        {"flight": "LA704",  "dep": "21:45", "arr": "13:55+1", "stops": 0, "equip": "B777-300ER",
         "seats": {"F": 6, "C": 35, "W": 24, "Y": 72, "M": 55, "K": 30, "V": 16, "N": 8}},
        {"flight": "IB6845", "dep": "16:30", "arr": "08:15+1", "stops": 0, "equip": "A330-300",
         "seats": {"F": 0, "C": 22, "W": 18, "Y": 48, "M": 35, "K": 20, "V": 10, "N": 4}},
    ],
    "GRU-MIA": [
        {"flight": "AA934",  "dep": "10:00", "arr": "18:40",   "stops": 0, "equip": "B767-300",
         "seats": {"F": 0, "C": 20, "W": 0,  "Y": 50, "M": 38, "K": 25, "V": 14, "N": 6}},
        {"flight": "LA646",  "dep": "22:30", "arr": "07:20+1", "stops": 1, "equip": "B787-8",
         "seats": {"F": 4, "C": 28, "W": 0,  "Y": 65, "M": 48, "K": 28, "V": 15, "N": 7}},
    ],
    "SCL-MIA": [
        {"flight": "LA800",  "dep": "16:30", "arr": "23:10",   "stops": 0, "equip": "A321XLR",
         "seats": {"F": 0, "C": 16, "W": 0,  "Y": 44, "M": 30, "K": 18, "V": 9,  "N": 3}},
        {"flight": "AA979",  "dep": "07:45", "arr": "18:25",   "stops": 1, "equip": "B737-900",
         "seats": {"F": 0, "C": 10, "W": 0,  "Y": 32, "M": 22, "K": 12, "V": 5,  "N": 1}},
    ],
    "BOG-MIA": [
        {"flight": "AV205",  "dep": "08:15", "arr": "12:30",   "stops": 0, "equip": "A320",
         "seats": {"F": 0, "C": 14, "W": 0,  "Y": 48, "M": 35, "K": 20, "V": 10, "N": 4}},
        {"flight": "AA927",  "dep": "14:50", "arr": "19:05",   "stops": 0, "equip": "B737-800",
         "seats": {"F": 0, "C": 8,  "W": 0,  "Y": 36, "M": 24, "K": 14, "V": 7,  "N": 2}},
    ],
}

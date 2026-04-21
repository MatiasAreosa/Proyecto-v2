from __future__ import annotations
import statistics
from datetime import datetime
from data.sample_data import (
    AIRPORTS, AIRLINES, ROUTE_FARES, CABIN_NAMES, FARE_BASIS,
    SAMPLE_PNRS, AVAILABILITY_TEMPLATE, get_bookings,
)

# ---------------------------------------------------------------------------
# Tool JSON schemas (Claude API format)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "buscar_disponibilidad",
        "description": (
            "Muestra disponibilidad de vuelos entre dos aeropuertos para una fecha dada, "
            "similar a un display de Sabre (1EZEJFK15MAR) o Amadeus (AN15MAREZEJFK). "
            "Devuelve vuelos disponibles con clases y asientos."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "origen": {"type": "string", "description": "Código IATA del aeropuerto de origen (ej: EZE, GRU)"},
                "destino": {"type": "string", "description": "Código IATA del aeropuerto de destino (ej: MAD, MIA)"},
                "fecha": {"type": "string", "description": "Fecha en formato DDMMM o DD/MM/YYYY (ej: 15MAR, 20/06/2025)"},
                "cabina": {"type": "string", "description": "Clase de cabina: F, C, W, Y, M, K, V, N (opcional)"},
                "aerolinea": {"type": "string", "description": "Código IATA de aerolínea para filtrar (ej: LA, AA) (opcional)"},
            },
            "required": ["origen", "destino", "fecha"],
        },
    },
    {
        "name": "analizar_reservas",
        "description": (
            "Analiza los datos de reservas por período, ruta, cabina u otros filtros. "
            "Calcula totales de revenue, pasajeros, promedios y tendencias."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mes": {"type": "integer", "description": "Mes a analizar (1-12). Si se omite, analiza todo el año."},
                "anio": {"type": "integer", "description": "Año a analizar (ej: 2024, 2025). Por defecto 2025."},
                "ruta": {"type": "string", "description": "Ruta en formato ORI-DST (ej: EZE-MAD). Opcional."},
                "cabina": {"type": "string", "description": "Filtrar por cabina: F, C, W, Y, M, K, V, N. Opcional."},
                "grupo_por": {
                    "type": "string",
                    "enum": ["mes", "ruta", "cabina", "aerolinea"],
                    "description": "Dimensión de agrupación para el análisis.",
                },
            },
            "required": ["anio"],
        },
    },
    {
        "name": "generar_reporte_mensual",
        "description": (
            "Genera un reporte mensual operacional o financiero con métricas clave: "
            "revenue total, pasajeros, load factor, RASK, yield, rutas top, etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mes": {"type": "integer", "description": "Mes del reporte (1-12)"},
                "anio": {"type": "integer", "description": "Año del reporte (ej: 2025)"},
                "tipo_reporte": {
                    "type": "string",
                    "enum": ["operacional", "financiero", "completo"],
                    "description": "Tipo de reporte a generar.",
                },
            },
            "required": ["mes", "anio"],
        },
    },
    {
        "name": "calcular_tarifa",
        "description": (
            "Calcula el desglose de tarifa para una ruta y cabina dadas, incluyendo "
            "tarifa base, tasas (YQ, impuestos locales) y total por pasajero y grupo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "origen": {"type": "string", "description": "Código IATA de origen (ej: EZE)"},
                "destino": {"type": "string", "description": "Código IATA de destino (ej: MAD)"},
                "cabina": {"type": "string", "description": "Clase de cabina: F, C, W, Y, M, K, V, N"},
                "base_tarifa": {"type": "string", "description": "Código de fare basis (ej: MLAOAP3M, YLAOAP). Opcional."},
                "num_adultos": {"type": "integer", "description": "Número de adultos (ADT). Por defecto 1."},
                "num_ninos": {"type": "integer", "description": "Número de niños (CNN, 75% de tarifa). Por defecto 0."},
                "num_infantes": {"type": "integer", "description": "Número de infantes (INF, 10% de tarifa). Por defecto 0."},
            },
            "required": ["origen", "destino", "cabina"],
        },
    },
    {
        "name": "interpretar_pnr",
        "description": (
            "Recupera y decodifica un PNR por su localizador. Muestra todos los elementos: "
            "itinerario, pasajeros, contacto, ticketing, SSRs, tarifas y observaciones."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "localizador": {"type": "string", "description": "Localizador del PNR (ej: ABC123, XYZ789)"},
            },
            "required": ["localizador"],
        },
    },
    {
        "name": "obtener_info_ruta",
        "description": (
            "Devuelve información detallada sobre aeropuertos y aerolíneas que operan "
            "una ruta: nombre, ciudad, país, zona, alianza, distancia estimada."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "origen": {"type": "string", "description": "Código IATA del aeropuerto de origen"},
                "destino": {"type": "string", "description": "Código IATA del aeropuerto de destino"},
            },
            "required": ["origen", "destino"],
        },
    },
    {
        "name": "calcular_metricas_revenue",
        "description": (
            "Calcula métricas de revenue management: RASK, CASK estimado, Load Factor, "
            "Yield, RevPAX y comparativa vs período anterior."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "mes": {"type": "integer", "description": "Mes (1-12). Si se omite, analiza todo el año."},
                "anio": {"type": "integer", "description": "Año (ej: 2025)"},
                "ruta": {"type": "string", "description": "Ruta ORI-DST para filtrar. Opcional (analiza toda la red)."},
            },
            "required": ["anio"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def buscar_disponibilidad(origen: str, destino: str, fecha: str,
                          cabina: str = "", aerolinea: str = "") -> str:
    origen = origen.upper().strip()
    destino = destino.upper().strip()
    cabina = cabina.upper().strip()
    aerolinea = aerolinea.upper().strip()

    key = f"{origen}-{destino}"
    avail = AVAILABILITY_TEMPLATE.get(key)

    if not avail:
        # Try to find fare data at least
        fare_key = f"{origen}-{destino}"
        if fare_key not in ROUTE_FARES:
            return (
                f"NO AVAILABILITY — Ruta {origen}-{destino} no encontrada en el sistema.\n"
                f"Rutas disponibles: {', '.join(AVAILABILITY_TEMPLATE.keys())}"
            )
        fares = ROUTE_FARES[fare_key]
        lines = [f"DISPLAY TARIFAS {origen}-{destino} / {fecha}",
                 "─" * 50,
                 "No hay vuelos simulados para esta ruta pero se encontraron tarifas:"]
        for cab, price in fares.items():
            lines.append(f"  {cab} ({CABIN_NAMES.get(cab, cab)}): USD {price:,.0f}")
        return "\n".join(lines)

    lines = [
        f"** DISPONIBILIDAD {origen} → {destino} / {fecha} **",
        f"{'#':<3} {'VLO':<8} {'SALE':<6} {'LLEGA':<6} {'EQP':<5} {'F':<4} {'C':<4} {'W':<4} {'Y':<4} {'M':<4} {'K':<4} {'V':<4} {'N':<4}",
        "─" * 72,
    ]

    # AVAILABILITY_TEMPLATE values are plain lists of flight dicts
    flights = avail if isinstance(avail, list) else avail.get("flights", [])
    if aerolinea:
        flights = [f for f in flights if f.get("flight", "").startswith(aerolinea)]

    if not flights:
        return f"SIN DISPONIBILIDAD para {origen}-{destino} en {fecha}" + (
            f" con aerolínea {aerolinea}" if aerolinea else ""
        )

    for i, flight in enumerate(flights, 1):
        seats = flight.get("seats", {})
        # Filter by cabin if requested
        if cabina and seats.get(cabina, 0) == 0:
            continue
        row = (
            f"{i:<3} {flight['flight']:<8} {flight['dep']:<6} {flight['arr']:<6} "
            f"{flight.get('equip', flight.get('equipment','738')):<5} "
            f"{seats.get('F',0):<4} {seats.get('C',0):<4} {seats.get('W',0):<4} "
            f"{seats.get('Y',0):<4} {seats.get('M',0):<4} {seats.get('K',0):<4} "
            f"{seats.get('V',0):<4} {seats.get('N',0):<4}"
        )
        lines.append(row)

    # Add fare reference
    fare_key = f"{origen}-{destino}"
    if fare_key in ROUTE_FARES:
        lines.append("")
        lines.append("TARIFAS DE REFERENCIA (USD):")
        for cab, price in ROUTE_FARES[fare_key].items():
            mark = " ◄" if cab == cabina else ""
            lines.append(f"  {cab} {CABIN_NAMES.get(cab, cab)}: {price:,.0f}{mark}")

    return "\n".join(lines)


def analizar_reservas(anio: int, mes: int = 0, ruta: str = "",
                      cabina: str = "", grupo_por: str = "mes") -> str:
    bookings = get_bookings(
        mes=mes if mes else None,
        anio=anio,
        ruta=ruta.upper() if ruta else None,
        cabina=cabina.upper() if cabina else None,
    )

    if not bookings:
        return f"No se encontraron reservas para los filtros indicados (año={anio}, mes={mes}, ruta={ruta})."

    total_rev = sum(b["revenue"] for b in bookings)
    total_pax = sum(b["total_pax"] for b in bookings)
    avg_lf = statistics.mean(b["load_factor"] for b in bookings)
    avg_fare = total_rev / total_pax if total_pax else 0

    # Group
    groups: dict[str, dict] = {}
    for b in bookings:
        if grupo_por == "mes":
            key = f"{b['anio']}-{b['mes']:02d}"
        elif grupo_por == "ruta":
            key = b["ruta"]
        elif grupo_por == "cabina":
            key = f"{b['cabina']} ({CABIN_NAMES.get(b['cabina'], b['cabina'])})"
        elif grupo_por == "aerolinea":
            key = b["aerolinea"]
        else:
            key = str(b["mes"])

        if key not in groups:
            groups[key] = {"revenue": 0, "pax": 0, "count": 0, "lf_sum": 0}
        groups[key]["revenue"] += b["revenue"]
        groups[key]["pax"] += b["total_pax"]
        groups[key]["count"] += 1
        groups[key]["lf_sum"] += b["load_factor"]

    lines = [
        f"=== ANÁLISIS DE RESERVAS — {anio}{f' / MES {mes}' if mes else ''} ===",
        f"Filtros: ruta={ruta or 'todas'}, cabina={cabina or 'todas'}, grupo por={grupo_por}",
        f"Total registros: {len(bookings):,}",
        f"Revenue total:   USD {total_rev:,.0f}",
        f"Pasajeros total: {total_pax:,}",
        f"Tarifa promedio: USD {avg_fare:,.0f}",
        f"Load Factor prom:{avg_lf:.1f}%",
        "",
        f"{'GRUPO':<20} {'REVENUE USD':>14} {'PAX':>8} {'LF%':>7} {'REGISTROS':>10}",
        "─" * 62,
    ]

    for key in sorted(groups):
        g = groups[key]
        lf = g["lf_sum"] / g["count"] if g["count"] else 0
        lines.append(
            f"{key:<20} {g['revenue']:>14,.0f} {g['pax']:>8,} {lf:>6.1f}% {g['count']:>10,}"
        )

    return "\n".join(lines)


def generar_reporte_mensual(mes: int, anio: int, tipo_reporte: str = "completo") -> str:
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
              "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    nombre_mes = meses[mes] if 1 <= mes <= 12 else str(mes)

    bookings = get_bookings(mes=mes, anio=anio)
    if not bookings:
        return f"Sin datos para {nombre_mes} {anio}."

    total_rev = sum(b["revenue"] for b in bookings)
    total_pax = sum(b["total_pax"] for b in bookings)
    avg_lf = statistics.mean(b["load_factor"] for b in bookings)
    avg_fare = total_rev / total_pax if total_pax else 0
    total_km = sum(b["km_vuelo"] * b["total_pax"] for b in bookings)  # RPK approx
    total_ask = sum(b["km_vuelo"] * b["asientos_avion"] for b in bookings)
    rask = total_rev / total_ask * 100 if total_ask else 0
    yield_val = total_rev / total_km * 100 if total_km else 0

    # By route
    rutas: dict[str, dict] = {}
    for b in bookings:
        r = b["ruta"]
        if r not in rutas:
            rutas[r] = {"rev": 0, "pax": 0}
        rutas[r]["rev"] += b["revenue"]
        rutas[r]["pax"] += b["total_pax"]
    top_rutas = sorted(rutas.items(), key=lambda x: x[1]["rev"], reverse=True)[:5]

    # By cabin
    cabinas: dict[str, dict] = {}
    for b in bookings:
        c = b["cabina"]
        if c not in cabinas:
            cabinas[c] = {"rev": 0, "pax": 0}
        cabinas[c]["rev"] += b["revenue"]
        cabinas[c]["pax"] += b["total_pax"]

    sep = "═" * 60
    lines = [
        sep,
        f"  REPORTE {tipo_reporte.upper()} — {nombre_mes.upper()} {anio}",
        sep,
    ]

    if tipo_reporte in ("operacional", "completo"):
        lines += [
            "",
            "── RESUMEN OPERACIONAL ──────────────────────────────────",
            f"  Registros de reserva:   {len(bookings):,}",
            f"  Pasajeros transportados:{total_pax:,}",
            f"  Load Factor promedio:   {avg_lf:.1f}%",
            f"  RPK (Miles aprox):      {total_km/1000:,.0f}k",
            f"  ASK (Miles aprox):      {total_ask/1000:,.0f}k",
            "",
            "  TOP 5 RUTAS POR REVENUE:",
            f"  {'RUTA':<12} {'REVENUE USD':>14} {'PAX':>8}",
            "  " + "─" * 36,
        ]
        for ruta, data in top_rutas:
            lines.append(f"  {ruta:<12} {data['rev']:>14,.0f} {data['pax']:>8,}")

    if tipo_reporte in ("financiero", "completo"):
        lines += [
            "",
            "── RESUMEN FINANCIERO ───────────────────────────────────",
            f"  Revenue Total:          USD {total_rev:,.0f}",
            f"  Tarifa Promedio:        USD {avg_fare:,.0f}",
            f"  RASK:                   {rask:.4f} USD/ASK×100",
            f"  Yield:                  {yield_val:.4f} USD/RPK×100",
            "",
            "  REVENUE POR CABINA:",
            f"  {'CABINA':<22} {'REVENUE USD':>14} {'PAX':>8} {'MIX%':>7}",
            "  " + "─" * 54,
        ]
        for cab in sorted(cabinas, key=lambda c: cabinas[c]["rev"], reverse=True):
            mix = cabinas[cab]["rev"] / total_rev * 100 if total_rev else 0
            lines.append(
                f"  {CABIN_NAMES.get(cab, cab):<22} {cabinas[cab]['rev']:>14,.0f} "
                f"{cabinas[cab]['pax']:>8,} {mix:>6.1f}%"
            )

    lines += ["", sep]
    return "\n".join(lines)


def calcular_tarifa(origen: str, destino: str, cabina: str,
                    base_tarifa: str = "", num_adultos: int = 1,
                    num_ninos: int = 0, num_infantes: int = 0) -> str:
    origen = origen.upper().strip()
    destino = destino.upper().strip()
    cabina = cabina.upper().strip()

    route_key = f"{origen}-{destino}"
    fares = ROUTE_FARES.get(route_key, {})
    if not fares:
        return f"Ruta {route_key} no encontrada. Rutas disponibles: {', '.join(ROUTE_FARES.keys())}"

    base = fares.get(cabina)
    if base is None:
        return f"Cabina '{cabina}' no disponible en {route_key}. Cabinas: {', '.join(fares.keys())}"

    # Tax logic: YQ ~25%, local taxes ~8%
    yq = round(base * 0.25)
    local_taxes = round(base * 0.08)
    total_adt = base + yq + local_taxes

    cnn_base = round(base * 0.75)
    total_cnn = cnn_base + yq + local_taxes

    inf_base = round(base * 0.10)
    total_inf = inf_base  # infants usually no YQ/taxes in sample

    grand_total = (total_adt * num_adultos) + (total_cnn * num_ninos) + (total_inf * num_infantes)

    # Fare basis info
    fb_info = ""
    if base_tarifa:
        fb = FARE_BASIS.get(base_tarifa.upper())
        if fb:
            fb_info = (
                f"\nFARE BASIS: {base_tarifa.upper()}\n"
                f"  Reembolsable:    {'Sí' if fb.get('refundable') else 'No'}\n"
                f"  Cambiable:       {'Sí' if fb.get('changeable') else 'No'}\n"
                f"  Anticipación:    {fb.get('advance_purchase', 'N/A')}\n"
                f"  Min estancia:    {fb.get('min_stay', 'N/A')}\n"
                f"  Max estancia:    {fb.get('max_stay', 'N/A')}\n"
                f"  Equipaje:        {fb.get('baggage', 'N/A')}"
            )

    lines = [
        f"=== COTIZACIÓN {route_key} / {CABIN_NAMES.get(cabina, cabina)} ({cabina}) ===",
        "",
        f"{'CONCEPTO':<30} {'ADT':>10} {'CNN':>10} {'INF':>10}",
        "─" * 62,
        f"{'Tarifa base':<30} {base:>10,.0f} {cnn_base:>10,.0f} {inf_base:>10,.0f}",
        f"{'YQ (fuel surcharge)':<30} {yq:>10,.0f} {yq:>10,.0f} {'0':>10}",
        f"{'Impuestos locales':<30} {local_taxes:>10,.0f} {local_taxes:>10,.0f} {'0':>10}",
        "─" * 62,
        f"{'TOTAL POR PAX (USD)':<30} {total_adt:>10,.0f} {total_cnn:>10,.0f} {total_inf:>10,.0f}",
        "",
        f"  Adultos ({num_adultos}):  USD {total_adt * num_adultos:,.0f}",
    ]
    if num_ninos:
        lines.append(f"  Niños   ({num_ninos}):  USD {total_cnn * num_ninos:,.0f}")
    if num_infantes:
        lines.append(f"  Infantes({num_infantes}):  USD {total_inf * num_infantes:,.0f}")
    lines += [
        "─" * 40,
        f"  TOTAL GRUPO:       USD {grand_total:,.0f}",
    ]
    if fb_info:
        lines.append(fb_info)

    return "\n".join(lines)


def interpretar_pnr(localizador: str) -> str:
    loc = localizador.upper().strip()
    pnr = SAMPLE_PNRS.get(loc)
    if not pnr:
        return (
            f"PNR '{loc}' no encontrado.\n"
            f"PNRs disponibles en el sistema de prueba: {', '.join(SAMPLE_PNRS.keys())}"
        )

    estado = pnr.get("estado") or pnr.get("status", "N/A")
    lines = [
        f"*** PNR — {loc} ***",
        f"Estado: {estado}",
    ]
    agente = pnr.get("agente") or pnr.get("agent")
    fecha = pnr.get("fecha_creacion") or pnr.get("created")
    if fecha:
        lines.append(f"Creado:  {fecha}  Agente: {agente or 'N/A'}")

    lines += ["", "PASAJEROS (NM):"]
    paxs = pnr.get("pasajeros") or pnr.get("passengers", [])
    for i, pax in enumerate(paxs, 1):
        # Support both Spanish and English keys
        name = (
            pax.get("name")
            or f"{pax.get('apellido','')}/{pax.get('nombre','')} {pax.get('titulo','')}"
        ).strip()
        ptc = pax.get("ptc") or pax.get("tipo", "ADT")
        tkt = pax.get("ticket", "SIN TICKET")
        fqtv = f"  FQTV: {pax['fqtv']}" if pax.get("fqtv") else ""
        lines.append(f"  {i}. {name} — {ptc} — Tkt: {tkt}{fqtv}")

    lines += ["", "ITINERARIO (AIR):"]
    segs = pnr.get("segmentos") or pnr.get("segments", [])
    for seg in segs:
        vuelo   = seg.get("flight") or seg.get("vuelo", "")
        clase   = seg.get("class")  or seg.get("clase", "")
        fecha_s = seg.get("date")   or seg.get("fecha", "")
        orig    = seg.get("from")   or seg.get("origen", "")
        dst     = seg.get("to")     or seg.get("destino", "")
        dep     = seg.get("dep")    or seg.get("hora_salida", "")
        arr     = seg.get("arr")    or seg.get("hora_llegada", "")
        st      = seg.get("status", "HK")
        lines.append(f"  {vuelo} {clase} {fecha_s} {orig}{dep} {dst}{arr} ST:{st}")

    contacto = pnr.get("contacto") or pnr.get("contact")
    if contacto:
        lines += ["", f"CONTACTO (AP): {contacto}"]

    tl = pnr.get("time_limit") or pnr.get("tiempo_limite")
    if tl:
        lines += [f"TICKETING (TK): TAW/{tl}"]

    fare = pnr.get("tarifa") or pnr.get("fare")
    if fare:
        lines += [
            "", "TARIFA (FP/FE):",
            f"  Base:   USD {fare.get('base', fare.get('tarifa_base', 0)):,.0f}",
            f"  Tasas:  USD {fare.get('taxes', fare.get('tasas', 0)):,.0f}",
            f"  Total:  USD {fare.get('total', 0):,.0f}",
            f"  Forma pago: {fare.get('form_of_payment', fare.get('forma_pago', 'N/A'))}",
        ]

    ssrs = pnr.get("ssrs") or pnr.get("servicios_especiales", [])
    if ssrs:
        lines += ["", "SSR / OSI:"]
        for ssr in ssrs:
            lines.append(f"  {ssr}")

    remarks = pnr.get("remarks") or pnr.get("observaciones", [])
    if remarks:
        lines += ["", "OBSERVACIONES (RM):"]
        for r in remarks:
            lines.append(f"  {r}")

    lines += ["", "*** END OF PNR ***"]
    return "\n".join(lines)


def obtener_info_ruta(origen: str, destino: str) -> str:
    origen = origen.upper().strip()
    destino = destino.upper().strip()

    orig_info = AIRPORTS.get(origen)
    dest_info = AIRPORTS.get(destino)

    if not orig_info:
        return f"Aeropuerto '{origen}' no encontrado. Disponibles: {', '.join(sorted(AIRPORTS.keys()))}"
    if not dest_info:
        return f"Aeropuerto '{destino}' no encontrado. Disponibles: {', '.join(sorted(AIRPORTS.keys()))}"

    route_key = f"{origen}-{destino}"
    fares = ROUTE_FARES.get(route_key, {})

    # Find airlines serving this route from sample bookings
    bookings = get_bookings(ruta=route_key)
    serving_airlines = list({b["aerolinea"] for b in bookings})

    lines = [
        f"=== INFORMACIÓN DE RUTA {route_key} ===",
        "",
        f"ORIGEN — {origen}:",
        f"  Nombre:  {orig_info['name']}",
        f"  Ciudad:  {orig_info['city']}, {orig_info['country']}",
        f"  Zona:    {orig_info['zone']}",
        "",
        f"DESTINO — {destino}:",
        f"  Nombre:  {dest_info['name']}",
        f"  Ciudad:  {dest_info['city']}, {dest_info['country']}",
        f"  Zona:    {dest_info['zone']}",
    ]

    if fares:
        lines += ["", "TARIFAS PUBLICADAS (USD):"]
        for cab, price in fares.items():
            lines.append(f"  {cab} — {CABIN_NAMES.get(cab, cab)}: {price:,.0f}")

    if serving_airlines:
        lines += ["", "AEROLÍNEAS CON OPERACIONES (datos muestra):"]
        for al_code in sorted(serving_airlines):
            al = AIRLINES.get(al_code, {})
            lines.append(
                f"  {al_code} — {al.get('name', al_code)} "
                f"(Alianza: {al.get('alliance', 'N/A')})"
            )

    return "\n".join(lines)


def calcular_metricas_revenue(anio: int, mes: int = 0, ruta: str = "") -> str:
    bookings = get_bookings(
        mes=mes if mes else None,
        anio=anio,
        ruta=ruta.upper() if ruta else None,
    )

    if not bookings:
        return "Sin datos para calcular métricas."

    # Current period
    total_rev = sum(b["revenue"] for b in bookings)
    total_pax = sum(b["total_pax"] for b in bookings)
    avg_lf = statistics.mean(b["load_factor"] for b in bookings)
    rpk = sum(b["km_vuelo"] * b["total_pax"] for b in bookings)
    ask = sum(b["km_vuelo"] * b["asientos_avion"] for b in bookings)
    rask = (total_rev / ask * 100) if ask else 0
    yield_val = (total_rev / rpk * 100) if rpk else 0
    rev_pax = total_rev / total_pax if total_pax else 0

    # Previous period for comparison
    prev_mes = mes - 1 if mes and mes > 1 else 12
    prev_anio = anio if (mes and mes > 1) else anio - 1
    prev_bookings = get_bookings(
        mes=prev_mes if mes else None,
        anio=prev_anio,
        ruta=ruta.upper() if ruta else None,
    )
    prev_rev = sum(b["revenue"] for b in prev_bookings) if prev_bookings else 0
    rev_var = ((total_rev - prev_rev) / prev_rev * 100) if prev_rev else 0
    prev_lf = statistics.mean(b["load_factor"] for b in prev_bookings) if prev_bookings else 0
    lf_var = avg_lf - prev_lf

    meses = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun",
              "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    periodo = f"{meses[mes]}/{anio}" if mes else str(anio)
    prev_periodo = f"{meses[prev_mes]}/{prev_anio}" if mes else str(prev_anio - 1)

    cask_est = rask * 0.75  # Estimated CASK as 75% of RASK

    lines = [
        f"=== MÉTRICAS REVENUE MANAGEMENT — {periodo}{f' / {ruta.upper()}' if ruta else ''} ===",
        "",
        f"{'MÉTRICA':<28} {'VALOR':>14} {'VS ' + prev_periodo:>12}",
        "─" * 56,
        f"{'Revenue Total (USD)':<28} {total_rev:>14,.0f} {rev_var:>+11.1f}%",
        f"{'Pasajeros':<28} {total_pax:>14,}",
        f"{'Load Factor (LF)':<28} {avg_lf:>13.1f}% {lf_var:>+11.1f}pp",
        f"{'RevPAX (USD/pax)':<28} {rev_pax:>14,.0f}",
        f"{'RPK (000)':<28} {rpk/1000:>14,.0f}",
        f"{'ASK (000)':<28} {ask/1000:>14,.0f}",
        f"{'RASK (USD/ASK×100)':<28} {rask:>14.4f}",
        f"{'Yield (USD/RPK×100)':<28} {yield_val:>14.4f}",
        f"{'CASK estimado (USD/ASK×100)':<28} {cask_est:>14.4f}",
        f"{'Margen RASK-CASK':<28} {rask - cask_est:>14.4f}",
        "",
        "NOTAS:",
        "  • CASK estimado al 75% del RASK (referencia; usar costos reales en producción)",
        "  • LF variación en puntos porcentuales (pp)",
        "  • RPK/ASK en miles de unidades",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dispatch map
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS: dict[str, callable] = {
    "buscar_disponibilidad": lambda inputs: buscar_disponibilidad(**inputs),
    "analizar_reservas": lambda inputs: analizar_reservas(**inputs),
    "generar_reporte_mensual": lambda inputs: generar_reporte_mensual(**inputs),
    "calcular_tarifa": lambda inputs: calcular_tarifa(**inputs),
    "interpretar_pnr": lambda inputs: interpretar_pnr(**inputs),
    "obtener_info_ruta": lambda inputs: obtener_info_ruta(**inputs),
    "calcular_metricas_revenue": lambda inputs: calcular_metricas_revenue(**inputs),
}

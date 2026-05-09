from __future__ import annotations

import csv
import random
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VENDOR_DIR = BASE_DIR / ".vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

OUT_SQL = BASE_DIR / "formula_none_seed.sql"
OUT_MD = BASE_DIR / "formula_none_data_sources.md"
SEED = 20260509
BALAPAN_ROW_LIMIT = 5000
RNG = random.Random(SEED)

try:
    from faker import Faker  # type: ignore
    from faker.config import AVAILABLE_LOCALES  # type: ignore

    fake = None
    faker_locale_codes: list[str] = []
except Exception:
    Faker = None  # type: ignore
    AVAILABLE_LOCALES = []  # type: ignore
    fake = None
    faker_locale_codes = []


FIRST_NAMES = [
    "Alex",
    "Amelia",
    "Andre",
    "Aisha",
    "Carlos",
    "Chloe",
    "Daniel",
    "Elena",
    "Ethan",
    "Fatima",
    "Gabriel",
    "Hannah",
    "Ivan",
    "Jasmine",
    "Kenji",
    "Laura",
    "Lucas",
    "Maya",
    "Naomi",
    "Omar",
    "Priya",
    "Rafael",
    "Sofia",
    "Victor",
]

LAST_NAMES = [
    "Adams",
    "Bennett",
    "Carter",
    "Chen",
    "Garcia",
    "Green",
    "Harris",
    "Johnson",
    "Kim",
    "Lee",
    "Lopez",
    "Martin",
    "Nguyen",
    "Patel",
    "Rossi",
    "Silva",
    "Smith",
    "Taylor",
    "Wilson",
    "Young",
]


COUNTRY_CODES = {
    "Argentina": "ARG",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",
    "Bahrain": "BHR",
    "Belgium": "BEL",
    "Brazil": "BRA",
    "Canada": "CAN",
    "Chile": "CHL",
    "China": "CHN",
    "Colombia": "COL",
    "Czech Republic": "CZE",
    "Denmark": "DNK",
    "Finland": "FIN",
    "France": "FRA",
    "Germany": "DEU",
    "Greece": "GRC",
    "Hong Kong": "HKG",
    "Hungary": "HUN",
    "India": "IND",
    "Indonesia": "IDN",
    "Ireland": "IRL",
    "Italy": "ITA",
    "Japan": "JPN",
    "Korea": "KOR",
    "Liechtenstein": "LIE",
    "Malaysia": "MYS",
    "Mexico": "MEX",
    "Monaco": "MCO",
    "Morocco": "MAR",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Qatar": "QAT",
    "Russia": "RUS",
    "Saudi Arabia": "SAU",
    "Singapore": "SGP",
    "South Africa": "ZAF",
    "Spain": "ESP",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "Thailand": "THA",
    "Turkey": "TUR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Uruguay": "URY",
    "Venezuela": "VEN",
    "Zimbabwe": "ZWE",
}


NATIONALITY_TO_COUNTRY = {
    "American": "United States",
    "American-Italian": "United States",
    "Argentine": "Argentina",
    "Argentine-Italian": "Argentina",
    "Argentinian": "Argentina",
    "Australian": "Australia",
    "Austrian": "Austria",
    "Belgian": "Belgium",
    "Brazilian": "Brazil",
    "British": "United Kingdom",
    "Canadian": "Canada",
    "Chilean": "Chile",
    "Chinese": "China",
    "Colombian": "Colombia",
    "Czech": "Czech Republic",
    "Danish": "Denmark",
    "Dutch": "Netherlands",
    "East German": "Germany",
    "Finnish": "Finland",
    "French": "France",
    "German": "Germany",
    "Hong Kong": "Hong Kong",
    "Hungarian": "Hungary",
    "Indian": "India",
    "Indonesian": "Indonesia",
    "Irish": "Ireland",
    "Italian": "Italy",
    "Japanese": "Japan",
    "Liechtensteiner": "Liechtenstein",
    "Malaysian": "Malaysia",
    "Mexican": "Mexico",
    "Monegasque": "Monaco",
    "New Zealander": "New Zealand",
    "Polish": "Poland",
    "Portuguese": "Portugal",
    "Rhodesian": "Zimbabwe",
    "Russian": "Russia",
    "South African": "South Africa",
    "Spanish": "Spain",
    "Swedish": "Sweden",
    "Swiss": "Switzerland",
    "Thai": "Thailand",
    "Uruguayan": "Uruguay",
    "Venezuelan": "Venezuela",
}


COUNTRY_TO_FAKER_LOCALES = {
    "Australia": ["en_AU"],
    "Austria": ["de_AT"],
    "Belgium": ["fr_BE", "nl_BE"],
    "Brazil": ["pt_BR"],
    "Canada": ["en_CA", "fr_CA"],
    "France": ["fr_FR"],
    "Germany": ["de_DE"],
    "Hong Kong": ["en"],
    "India": ["en_IN"],
    "Ireland": ["en_IE", "ga_IE"],
    "Italy": ["it_IT"],
    "Japan": ["en"],
    "Malaysia": ["en_MS"],
    "Mexico": ["es_MX"],
    "Netherlands": ["nl_NL"],
    "New Zealand": ["en_NZ"],
    "Russia": ["en"],
    "South Africa": ["zu_ZA", "en"],
    "Spain": ["es_ES"],
    "Switzerland": ["de_CH", "fr_CH", "it_CH"],
    "United Kingdom": ["en_GB"],
    "United States": ["en_US"],
    "Zimbabwe": ["en_GB"],
}


SPECIALTIES = [
    "Track",
    "Pit lane",
    "Recovery vehicle",
    "Fire safety",
    "Medical response",
    "Flag marshal",
    "Grid marshal",
    "Scrutineering support",
    "Radio communication",
    "Incident command",
]

CERTIFICATION_LEVELS = ["Grade 1", "Grade 2", "Grade 3", "Senior", "Chief"]


def read_csv(filename: str) -> list[dict[str, str]]:
    path = BASE_DIR / filename
    if not path.exists():
        path = DATA_DIR / filename
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text == r"\N":
        return None
    return text


def int_or_none(value: object) -> int | None:
    text = clean(value)
    if text is None:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def float_or_zero(value: object) -> float:
    text = clean(value)
    if text is None:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def normalize_country(value: object) -> str:
    text = clean(value)
    if text is None:
        return "Unknown"
    text = " ".join(text.split())
    aliases = {
        "UK": "United Kingdom",
        "USA": "United States",
        "UAE": "United Arab Emirates",
    }
    return aliases.get(text, NATIONALITY_TO_COUNTRY.get(text, text))


def country_code(country: str) -> str:
    if country in COUNTRY_CODES:
        return COUNTRY_CODES[country]
    letters = "".join(ch for ch in country.upper() if ch.isalpha())
    return (letters[:3] or "UNK").ljust(3, "X")


def driver_name(row: dict[str, str]) -> str:
    name = f"{clean(row.get('forename')) or 'Unknown'} {clean(row.get('surname')) or 'Driver'}"
    return " ".join(name.split())


def make_unique_names(
    rows: list[dict[str, str]],
    id_key: str,
    base_name,
) -> dict[str, str]:
    counts: dict[str, int] = defaultdict(int)
    result: dict[str, str] = {}
    for row in rows:
        key = clean(row.get(id_key))
        if key is None:
            continue
        base = clean(base_name(row)) or f"Unknown {key}"
        counts[base] += 1
        result[key] = base if counts[base] == 1 else f"{base} {key}"
    return result


def unique_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def uses_latin_alphabet(text: str) -> bool:
    for character in text:
        if character.isalpha() and "LATIN" not in unicodedata.name(character, ""):
            return False
    return True


def faker_locales_for_team_countries(constructors: list[dict[str, str]]) -> list[str]:
    team_countries = unique_preserve_order(
        [
            normalize_country(row.get("nationality"))
            for row in constructors
            if clean(row.get("nationality")) is not None
        ]
    )
    locale_candidates = []
    for country in team_countries:
        locale_candidates.extend(COUNTRY_TO_FAKER_LOCALES.get(country, ["en"]))

    available = set(AVAILABLE_LOCALES)
    locales = [locale for locale in locale_candidates if locale in available]
    return unique_preserve_order(locales) or ["en"]


def init_faker_for_team_countries(constructors: list[dict[str, str]]) -> None:
    global fake, faker_locale_codes
    if Faker is None:
        return
    faker_locale_codes = faker_locales_for_team_countries(constructors)
    fake = Faker(faker_locale_codes)
    Faker.seed(SEED)


def sql_value(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    return "'" + text.replace("\\", "\\\\").replace("'", "''") + "'"


def write_insert(handle, table: str, columns: list[str], rows: list[tuple], chunk_size: int = 500) -> None:
    if not rows:
        return
    handle.write(f"\n-- {table}: {len(rows)} rows\n")
    col_sql = ", ".join(columns)
    for start in range(0, len(rows), chunk_size):
        chunk = rows[start : start + chunk_size]
        handle.write(f"INSERT INTO {table} ({col_sql}) VALUES\n")
        values = []
        for row in chunk:
            values.append("    (" + ", ".join(sql_value(value) for value in row) + ")")
        handle.write(",\n".join(values))
        handle.write(";\n")


def synthetic_person_name(index: int) -> str:
    if fake is not None:
        for _ in range(50):
            name = fake.name()
            if uses_latin_alphabet(name):
                return name
    first = FIRST_NAMES[index % len(FIRST_NAMES)]
    last = LAST_NAMES[(index * 7) % len(LAST_NAMES)]
    middle = LAST_NAMES[(index * 11 + 3) % len(LAST_NAMES)]
    return f"{first} {middle} {last}"


def synthetic_principal(index: int) -> str:
    if fake is not None:
        for _ in range(50):
            name = fake.name()
            if uses_latin_alphabet(name):
                return name
    return synthetic_person_name(index + 500)


def datetime_value(date_value: object, time_value: object) -> str | None:
    date_text = clean(date_value)
    if date_text is None:
        return None
    time_text = clean(time_value) or "00:00:00"
    return f"{date_text} {time_text}"


def build_seed_data() -> tuple[dict[str, list[tuple]], dict[str, int]]:
    circuits = read_csv("circuits.csv")
    constructors = read_csv("constructors.csv")
    init_faker_for_team_countries(constructors)
    drivers = read_csv("drivers.csv")
    seasons = read_csv("seasons.csv")
    races = read_csv("races.csv")
    results = read_csv("results.csv")
    qualifying = read_csv("qualifying.csv")
    constructor_results = read_csv("constructor_results.csv")
    statuses = read_csv("status.csv")

    circuit_names = make_unique_names(circuits, "circuitId", lambda row: clean(row.get("name")))
    constructor_names = make_unique_names(constructors, "constructorId", lambda row: clean(row.get("name")))
    driver_names = make_unique_names(drivers, "driverId", driver_name)

    races_by_id = {clean(row.get("raceId")): row for row in races if clean(row.get("raceId"))}
    circuits_by_id = {clean(row.get("circuitId")): row for row in circuits if clean(row.get("circuitId"))}
    constructors_by_id = {
        clean(row.get("constructorId")): row for row in constructors if clean(row.get("constructorId"))
    }
    drivers_by_id = {clean(row.get("driverId")): row for row in drivers if clean(row.get("driverId"))}
    status_by_id = {
        clean(row.get("statusId")): clean(row.get("status")) or "Unknown"
        for row in statuses
        if clean(row.get("statusId"))
    }

    gp_names: dict[str, str] = {}
    gp_counts: dict[str, int] = defaultdict(int)
    for race in races:
        race_id = clean(race.get("raceId"))
        if race_id is None:
            continue
        base = f"{clean(race.get('year'))} {clean(race.get('name')) or 'Grand Prix'}"
        gp_counts[base] += 1
        if gp_counts[base] > 1:
            base = f"{base} Round {clean(race.get('round')) or race_id}"
        gp_names[race_id] = base

    all_countries = set()
    for row in circuits:
        all_countries.add(normalize_country(row.get("country")))
    for row in constructors:
        all_countries.add(normalize_country(row.get("nationality")))
    for row in drivers:
        all_countries.add(normalize_country(row.get("nationality")))

    negara_rows = [(country, country_code(country)) for country in sorted(all_countries) if country != "Unknown"]
    musim_values = sorted(
        {
            int_or_none(row.get("year"))
            for row in seasons
        }
        | {
            int_or_none(row.get("year"))
            for row in races
        }
    )
    musim_rows = [(year,) for year in musim_values if year is not None]

    sirkuit_rows = []
    for index, row in enumerate(circuits):
        circuit_id = clean(row.get("circuitId"))
        if circuit_id is None:
            continue
        length = round(RNG.uniform(3.100, 7.200), 3)
        corners = RNG.randint(8, 24)
        sirkuit_rows.append(
            (
                circuit_names[circuit_id],
                f"{length:.3f}",
                corners,
                normalize_country(row.get("country")),
            )
        )

    tim_rows = []
    for index, row in enumerate(constructors):
        constructor_id = clean(row.get("constructorId"))
        if constructor_id is None:
            continue
        budget = RNG.randint(75_000_000, 475_000_000)
        tim_rows.append(
            (
                constructor_names[constructor_id],
                synthetic_principal(index),
                f"{budget:.2f}",
                normalize_country(row.get("nationality")),
            )
        )

    pemasok_rows = []
    for row in constructors:
        constructor_id = clean(row.get("constructorId"))
        if constructor_id is None:
            continue
        pemasok_rows.append(
            (
                constructor_names[constructor_id],
                normalize_country(row.get("nationality")),
            )
        )

    marshal_names: list[str] = []
    used_marshal_names: set[str] = set()
    for index in range(120):
        name = synthetic_person_name(index)
        if name in used_marshal_names:
            name = f"{name} {index + 1}"
        used_marshal_names.add(name)
        marshal_names.append(name)
    marshal_rows = [
        (name, CERTIFICATION_LEVELS[index % len(CERTIFICATION_LEVELS)])
        for index, name in enumerate(marshal_names)
    ]

    pembalap_rows = []
    for row in drivers:
        driver_id = clean(row.get("driverId"))
        if driver_id is None:
            continue
        number = int_or_none(row.get("number"))
        if number is None:
            number = RNG.randint(1, 99)
        pembalap_rows.append(
            (
                driver_names[driver_id],
                number if 0 <= number <= 255 else RNG.randint(1, 99),
                normalize_country(row.get("nationality")),
            )
        )

    driver_first_year: dict[str, int] = {}
    driver_last_year: dict[str, int] = {}
    for row in results:
        driver_id = clean(row.get("driverId"))
        race = races_by_id.get(clean(row.get("raceId")))
        if driver_id is None or race is None:
            continue
        year = int_or_none(race.get("year"))
        if year is None:
            continue
        driver_first_year[driver_id] = min(driver_first_year.get(driver_id, year), year)
        driver_last_year[driver_id] = max(driver_last_year.get(driver_id, year), year)

    max_year = max(int_or_none(row.get("year")) or 0 for row in races)
    threshold = max_year - 4
    active_ids = [driver_id for driver_id, year in driver_last_year.items() if year >= threshold]
    while len(active_ids) < 50 and threshold > 1950:
        threshold -= 1
        active_ids = [driver_id for driver_id, year in driver_last_year.items() if year >= threshold]

    active_id_set = set(active_ids)
    pembalap_aktif_rows = [
        (
            driver_names[driver_id],
            driver_first_year.get(driver_id),
            "Aktif" if index % 5 else "Bebas Transfer",
        )
        for index, driver_id in enumerate(sorted(active_id_set, key=lambda item: driver_names[item]))
    ]
    pembalap_pensiun_rows = [
        (
            driver_names[driver_id],
            driver_last_year.get(driver_id),
        )
        for driver_id in sorted(driver_last_year, key=lambda item: driver_names[item])
        if driver_id not in active_id_set
    ]

    team_years: set[tuple[str, int]] = set()
    for row in constructor_results:
        constructor_id = clean(row.get("constructorId"))
        race = races_by_id.get(clean(row.get("raceId")))
        if constructor_id is None or race is None:
            continue
        year = int_or_none(race.get("year"))
        if year is not None:
            team_years.add((constructor_id, year))

    supplier_ids = sorted(constructors_by_id, key=lambda value: int_or_none(value) or 0)
    memasok_rows = []
    for constructor_id, year in sorted(team_years, key=lambda item: (item[1], int_or_none(item[0]) or 0)):
        team_name = constructor_names.get(constructor_id)
        if team_name is None:
            continue
        supplier_index = ((int_or_none(constructor_id) or 0) * 31 + year) % len(supplier_ids)
        supplier_id = supplier_ids[supplier_index]
        memasok_rows.append((constructor_names[supplier_id], team_name, year))

    contract_set: set[tuple[str, str, int]] = set()
    for row in results:
        constructor_id = clean(row.get("constructorId"))
        driver_id = clean(row.get("driverId"))
        race = races_by_id.get(clean(row.get("raceId")))
        if constructor_id is None or driver_id is None or race is None:
            continue
        year = int_or_none(race.get("year"))
        if year is None:
            continue
        team_name = constructor_names.get(constructor_id)
        racer_name = driver_names.get(driver_id)
        if team_name is not None and racer_name is not None:
            contract_set.add((team_name, racer_name, year))
    kontrak_rows = sorted(contract_set, key=lambda row: (row[2], row[0], row[1]))

    grand_prix_rows = []
    for race in races:
        race_id = clean(race.get("raceId"))
        circuit_id = clean(race.get("circuitId"))
        year = int_or_none(race.get("year"))
        if race_id is None or circuit_id is None or year is None:
            continue
        circuit_name = circuit_names.get(circuit_id)
        if circuit_name is not None:
            grand_prix_rows.append((gp_names[race_id], circuit_name, year))

    session_specs = [
        ("FP1", "fp1_date", "fp1_time", 60),
        ("FP2", "fp2_date", "fp2_time", 60),
        ("FP3", "fp3_date", "fp3_time", 60),
        ("Kualifikasi", "quali_date", "quali_time", 60),
        ("Sprint", "sprint_date", "sprint_time", 30),
        ("Race", "date", "time", 120),
    ]
    sesi_rows = []
    for race in races:
        race_id = clean(race.get("raceId"))
        if race_id is None:
            continue
        gp_name = gp_names[race_id]
        for session_name, date_col, time_col, duration in session_specs:
            if session_name != "Race" and clean(race.get(date_col)) is None:
                continue
            sesi_rows.append(
                (
                    session_name,
                    gp_name,
                    datetime_value(race.get(date_col), race.get(time_col)),
                    duration,
                )
            )

    balapan_map: dict[tuple[str, str], tuple[tuple, tuple[float, int, int], tuple[int, int, int]]] = {}
    for row in results:
        driver_id = clean(row.get("driverId"))
        race_id = clean(row.get("raceId"))
        if driver_id is None or race_id is None:
            continue
        racer_name = driver_names.get(driver_id)
        gp_name = gp_names.get(race_id)
        if racer_name is None or gp_name is None:
            continue
        position = int_or_none(row.get("positionOrder"))
        time_text = clean(row.get("time")) or status_by_id.get(clean(row.get("statusId")), "DNF")
        time_text = time_text[:20] if time_text else None
        points = f"{float_or_zero(row.get('points')):.2f}"
        laps = int_or_none(row.get("laps")) or 0
        key = (racer_name, gp_name)
        output_row = (racer_name, gp_name, position, time_text, points)
        score = (float(points), -(position or 999), laps)
        race = races_by_id.get(race_id)
        race_year = int_or_none(race.get("year")) if race is not None else None
        race_round = int_or_none(race.get("round")) if race is not None else None
        result_id = int_or_none(row.get("resultId")) or 0
        sort_key = (race_year or 0, race_round or 0, result_id)
        if key not in balapan_map or score > balapan_map[key][1]:
            balapan_map[key] = (output_row, score, sort_key)
    selected_balapan = sorted(balapan_map.values(), key=lambda item: item[2], reverse=True)[:BALAPAN_ROW_LIMIT]
    balapan_rows = sorted((item[0] for item in selected_balapan), key=lambda row: (row[1], row[2] or 999, row[0]))
    balapan_keys = {(row[0], row[1]) for row in balapan_rows}

    awards: set[tuple[str, str, str, str]] = set()
    for row in results:
        driver_id = clean(row.get("driverId"))
        race_id = clean(row.get("raceId"))
        racer_name = driver_names.get(driver_id or "")
        gp_name = gp_names.get(race_id or "")
        if racer_name is None or gp_name is None or (racer_name, gp_name) not in balapan_keys:
            continue
        if int_or_none(row.get("positionOrder")) == 1:
            awards.add(("Pemenang Balapan", racer_name, gp_name, f"Menang pada {gp_name}."))
        if int_or_none(row.get("rank")) == 1:
            lap_time = clean(row.get("fastestLapTime")) or "waktu tercepat"
            awards.add(("Fastest Lap", racer_name, gp_name, f"Mencatat fastest lap {lap_time}."))

    for row in qualifying:
        if int_or_none(row.get("position")) != 1:
            continue
        driver_id = clean(row.get("driverId"))
        race_id = clean(row.get("raceId"))
        racer_name = driver_names.get(driver_id or "")
        gp_name = gp_names.get(race_id or "")
        if racer_name is None or gp_name is None or (racer_name, gp_name) not in balapan_keys:
            continue
        q_time = clean(row.get("q3")) or clean(row.get("q2")) or clean(row.get("q1")) or "waktu terbaik"
        awards.add(("Pole Position", racer_name, gp_name, f"Start posisi pertama dengan {q_time}."))
    penghargaan_rows = sorted(awards, key=lambda row: (row[2], row[0], row[1]))

    spesialisasi_rows = []
    for index, name in enumerate(marshal_names):
        count = 1 + (index % 3)
        for offset in range(count):
            specialty = SPECIALTIES[(index + offset * 3) % len(SPECIALTIES)]
            spesialisasi_rows.append((name, specialty))

    menjaga_rows = []
    for index, row in enumerate(sesi_rows):
        session_name, gp_name = row[0], row[1]
        count = 3 if session_name == "Race" else 2
        selected = set()
        for offset in range(count):
            marshal = marshal_names[(index * 7 + offset * 13) % len(marshal_names)]
            if marshal in selected:
                continue
            selected.add(marshal)
            menjaga_rows.append((gp_name, session_name, marshal))

    rows_by_table = {
        "Negara": negara_rows,
        "Musim": musim_rows,
        "Sirkuit": sirkuit_rows,
        "Tim": tim_rows,
        "Pemasok_mesin": pemasok_rows,
        "Marshal": marshal_rows,
        "Pembalap": pembalap_rows,
        "Pembalap_aktif": pembalap_aktif_rows,
        "Pembalap_pensiun": pembalap_pensiun_rows,
        "Memasok": memasok_rows,
        "Kontrak": kontrak_rows,
        "Grand_prix": grand_prix_rows,
        "Sesi": sesi_rows,
        "Balapan": balapan_rows,
        "Penghargaan": penghargaan_rows,
        "Spesialisasi_marshal": spesialisasi_rows,
        "Menjaga": menjaga_rows,
    }
    counts = {table: len(rows) for table, rows in rows_by_table.items()}
    return rows_by_table, counts


def write_sql(rows_by_table: dict[str, list[tuple]]) -> None:
    columns = {
        "Negara": ["nama", "kode"],
        "Musim": ["tahun"],
        "Sirkuit": ["nama", "panjang_lintasan", "jumlah_tikungan", "negara"],
        "Tim": ["nama", "prinsipal_tim", "anggaran_musim", "negara"],
        "Pemasok_mesin": ["nama", "negara"],
        "Marshal": ["nama", "level_sertifikasi"],
        "Pembalap": ["nama", "no_balap", "negara"],
        "Pembalap_aktif": ["nama_pembalap", "tahun_debut", "status_kontrak"],
        "Pembalap_pensiun": ["nama_pembalap", "tahun_pensiun"],
        "Memasok": ["nama_pemasok", "nama_tim", "musim"],
        "Kontrak": ["nama_tim", "nama_pembalap", "musim"],
        "Grand_prix": ["nama_grandprix", "sirkuit", "musim"],
        "Sesi": ["nama", "grandprix", "waktu_mulai", "durasi"],
        "Balapan": ["pembalap", "grandprix", "posisi_finish", "waktu_tempuh", "poin"],
        "Penghargaan": ["nama_penghargaan", "nama_pembalap", "grandprix", "deskripsi"],
        "Spesialisasi_marshal": ["nama_marshal", "spesialisasi"],
        "Menjaga": ["nama_grandprix", "nama_sesi", "nama_marshal"],
    }

    order = [
        "Negara",
        "Musim",
        "Sirkuit",
        "Tim",
        "Pemasok_mesin",
        "Marshal",
        "Pembalap",
        "Pembalap_aktif",
        "Pembalap_pensiun",
        "Memasok",
        "Kontrak",
        "Grand_prix",
        "Sesi",
        "Balapan",
        "Penghargaan",
        "Spesialisasi_marshal",
        "Menjaga",
    ]

    with OUT_SQL.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("-- Formula None seed data generated from Kaggle F1 CSV files.\n")
        handle.write("-- Run after formula_none.sql on MariaDB 10.6.2 or newer.\n\n")
        handle.write("USE formula_none;\n")
        handle.write("SET NAMES utf8mb4;\n")
        handle.write("START TRANSACTION;\n")
        for table in order:
            write_insert(handle, table, columns[table], rows_by_table[table])
        handle.write("\nCOMMIT;\n")


def write_markdown(counts: dict[str, int]) -> None:
    faker_status = (
        "Python Faker package with locales derived from constructor/team countries: "
        + ", ".join(faker_locale_codes)
        if fake is not None
        else "deterministic fallback with Faker-like fields"
    )
    lines = [
        "# Formula None CSV Availability",
        "",
        f"Generated by `generate_formula_none_seed.py` using seed `{SEED}`.",
        f"Faker source used for non-CSV fields: {faker_status}.",
        "",
        "## Table Source Mapping",
        "",
        "| Tabel | Status di CSV | Sumber / metode |",
        "| --- | --- | --- |",
        "| Negara | Tersedia | Dari `circuits.country`, `drivers.nationality`, dan `constructors.nationality`, lalu dinormalisasi ke nama negara. Kolom `kode` dibuat dari mapping ISO. |",
        "| Musim | Tersedia | Dari `seasons.year` dan `races.year`. |",
        "| Sirkuit | Tersedia sebagian | `circuits.name` dan `circuits.country`; panjang lintasan dan jumlah tikungan dibuat sintetis karena tidak ada di CSV. |",
        "| Tim | Tersedia sebagian | Dari `constructors.name` dan `constructors.nationality`; prinsipal tim dan anggaran dibuat sintetis. |",
        "| Pemasok_mesin | Tidak eksplisit | Dataset tidak punya tabel engine supplier; nama dan negara memakai `constructors.csv` sebagai proxy manufaktur/pemasok. |",
        "| Memasok | Tidak eksplisit | Dataset tidak punya relasi pemasok mesin ke tim; tim-musim diambil dari `constructor_results.csv`, pemasok dipasangkan secara deterministik. |",
        "| Pembalap | Tersedia | Dari `drivers.csv`, termasuk nomor balap jika ada. |",
        "| Pembalap_aktif | Tidak eksplisit | Tidak ada status aktif; diinfer dari pembalap dengan tahun balapan terakhir pada periode terbaru dataset. |",
        "| Pembalap_pensiun | Tidak eksplisit | Tidak ada status pensiun; diinfer dari pembalap yang tidak masuk kelompok aktif. |",
        "| Kontrak | Tersedia sebagai hasil join | Dari kombinasi `results.driverId`, `results.constructorId`, dan `races.year`. |",
        "| Grand_prix | Tersedia | Dari `races.name`, `races.year`, dan `races.circuitId`. |",
        "| Sesi | Tersedia sebagian | `races.csv` punya tanggal/jam FP, kualifikasi, sprint, dan race; durasi sesi dibuat sintetis standar. |",
        "| Balapan | Tersedia | Dari `results.csv`, join ke `drivers.csv` dan `races.csv`. |",
        "| Penghargaan | Tidak eksplisit | Diinfer dari `results.csv` dan `qualifying.csv`: pemenang balapan, fastest lap, dan pole position. |",
        "| Marshal | Tidak tersedia | Dibuat dengan Faker/fallback sintetis. |",
        "| Spesialisasi_marshal | Tidak tersedia | Dibuat sintetis dari daftar spesialisasi marshal. |",
        "| Menjaga | Tidak tersedia | Dibuat sintetis dengan memasangkan marshal ke sesi. |",
        "",
        "## Generated Row Counts",
        "",
        "| Tabel | Jumlah row |",
        "| --- | ---: |",
    ]
    for table in [
        "Negara",
        "Musim",
        "Sirkuit",
        "Tim",
        "Pemasok_mesin",
        "Marshal",
        "Pembalap",
        "Pembalap_aktif",
        "Pembalap_pensiun",
        "Memasok",
        "Kontrak",
        "Grand_prix",
        "Sesi",
        "Balapan",
        "Penghargaan",
        "Spesialisasi_marshal",
        "Menjaga",
    ]:
        lines.append(f"| {table} | {counts[table]} |")
    lines.append("")
    lines.append("## Import Order")
    lines.append("")
    lines.append("1. Jalankan `formula_none.sql` untuk membuat database, tabel, constraint, dan view.")
    lines.append("2. Jalankan `formula_none_seed.sql` untuk mengisi data.")
    lines.append("")
    lines.append("## Regenerate Seed")
    lines.append("")
    lines.append("1. Jalankan `python -m venv .venv-faker`.")
    lines.append("2. Jalankan `.\\.venv-faker\\bin\\python.exe -m pip install -r requirements.txt`.")
    lines.append("3. Jalankan `.\\.venv-faker\\bin\\python.exe generate_formula_none_seed.py`.")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def ensure_unique(table: str, rows: list[tuple], key_indexes: tuple[int, ...]) -> None:
    seen = set()
    for row in rows:
        key = tuple(row[index] for index in key_indexes)
        if key in seen:
            raise ValueError(f"Duplicate primary key in {table}: {key}")
        seen.add(key)


def validate_seed(rows_by_table: dict[str, list[tuple]]) -> None:
    minimums = {
        "Negara": 20,
        "Musim": 20,
        "Marshal": 20,
        "Sirkuit": 50,
        "Tim": 50,
        "Pemasok_mesin": 50,
        "Pembalap": 50,
        "Pembalap_aktif": 50,
        "Pembalap_pensiun": 50,
        "Memasok": 150,
        "Kontrak": 150,
        "Grand_prix": 100,
        "Sesi": 50,
        "Balapan": 100,
        "Penghargaan": 50,
        "Spesialisasi_marshal": 50,
        "Menjaga": 100,
    }
    for table, minimum in minimums.items():
        actual = len(rows_by_table[table])
        if actual < minimum:
            raise ValueError(f"{table} has {actual} rows, below required minimum {minimum}")

    primary_keys = {
        "Negara": (0,),
        "Musim": (0,),
        "Sirkuit": (0,),
        "Tim": (0,),
        "Pemasok_mesin": (0,),
        "Marshal": (0,),
        "Pembalap": (0,),
        "Pembalap_aktif": (0,),
        "Pembalap_pensiun": (0,),
        "Memasok": (0, 1, 2),
        "Kontrak": (0, 1, 2),
        "Grand_prix": (0,),
        "Sesi": (0, 1),
        "Balapan": (0, 1),
        "Penghargaan": (0, 1, 2),
        "Spesialisasi_marshal": (0, 1),
        "Menjaga": (0, 1, 2),
    }
    for table, key_indexes in primary_keys.items():
        ensure_unique(table, rows_by_table[table], key_indexes)

    negara = {row[0] for row in rows_by_table["Negara"]}
    musim = {row[0] for row in rows_by_table["Musim"]}
    sirkuit = {row[0] for row in rows_by_table["Sirkuit"]}
    tim = {row[0] for row in rows_by_table["Tim"]}
    pemasok = {row[0] for row in rows_by_table["Pemasok_mesin"]}
    marshal = {row[0] for row in rows_by_table["Marshal"]}
    pembalap = {row[0] for row in rows_by_table["Pembalap"]}
    grand_prix = {row[0] for row in rows_by_table["Grand_prix"]}
    sesi = {(row[0], row[1]) for row in rows_by_table["Sesi"]}
    balapan = {(row[0], row[1]) for row in rows_by_table["Balapan"]}

    checks = [
        ("Sirkuit.negara", all(row[3] in negara for row in rows_by_table["Sirkuit"])),
        ("Tim.negara", all(row[3] in negara for row in rows_by_table["Tim"])),
        ("Pemasok_mesin.negara", all(row[1] in negara for row in rows_by_table["Pemasok_mesin"])),
        ("Pembalap.negara", all(row[2] in negara for row in rows_by_table["Pembalap"])),
        ("Pembalap_aktif.nama_pembalap", all(row[0] in pembalap for row in rows_by_table["Pembalap_aktif"])),
        ("Pembalap_pensiun.nama_pembalap", all(row[0] in pembalap for row in rows_by_table["Pembalap_pensiun"])),
        ("Memasok.nama_pemasok", all(row[0] in pemasok for row in rows_by_table["Memasok"])),
        ("Memasok.nama_tim", all(row[1] in tim for row in rows_by_table["Memasok"])),
        ("Memasok.musim", all(row[2] in musim for row in rows_by_table["Memasok"])),
        ("Kontrak.nama_tim", all(row[0] in tim for row in rows_by_table["Kontrak"])),
        ("Kontrak.nama_pembalap", all(row[1] in pembalap for row in rows_by_table["Kontrak"])),
        ("Kontrak.musim", all(row[2] in musim for row in rows_by_table["Kontrak"])),
        ("Grand_prix.sirkuit", all(row[1] in sirkuit for row in rows_by_table["Grand_prix"])),
        ("Grand_prix.musim", all(row[2] in musim for row in rows_by_table["Grand_prix"])),
        ("Sesi.grandprix", all(row[1] in grand_prix for row in rows_by_table["Sesi"])),
        ("Balapan.pembalap", all(row[0] in pembalap for row in rows_by_table["Balapan"])),
        ("Balapan.grandprix", all(row[1] in grand_prix for row in rows_by_table["Balapan"])),
        ("Penghargaan.balapan", all((row[1], row[2]) in balapan for row in rows_by_table["Penghargaan"])),
        ("Spesialisasi_marshal.nama_marshal", all(row[0] in marshal for row in rows_by_table["Spesialisasi_marshal"])),
        ("Menjaga.sesi", all((row[1], row[0]) in sesi for row in rows_by_table["Menjaga"])),
        ("Menjaga.marshal", all(row[2] in marshal for row in rows_by_table["Menjaga"])),
    ]
    failures = [name for name, ok in checks if not ok]
    if failures:
        raise ValueError("Foreign key validation failed: " + ", ".join(failures))


def main() -> None:
    rows_by_table, counts = build_seed_data()
    validate_seed(rows_by_table)
    write_sql(rows_by_table)
    write_markdown(counts)
    print(f"Wrote {OUT_SQL.name}")
    print(f"Wrote {OUT_MD.name}")
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()

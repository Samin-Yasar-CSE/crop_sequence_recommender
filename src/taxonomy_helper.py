# src/taxonomy_helper.py
import os
import csv
import json
import glob
import re
from typing import Any, Dict

# ==============================================================================
# 1. COMPREHENSIVE BACKUP DICTIONARY (Bangladesh BARC + Global Common Crops)
# ==============================================================================
BACKUP_FAMILY_DICT: Dict[str, str] = {
    # --- Fabaceae (Legumes / Pulses - Nitrogen Fixing) ---
    "cowpea": "Fabaceae", "felon": "Fabaceae", "black eyed pea": "Fabaceae",
    "mungbean": "Fabaceae", "mung bean": "Fabaceae", "green gram": "Fabaceae", "moog": "Fabaceae",
    "blackgram": "Fabaceae", "black gram": "Fabaceae", "mashkalai": "Fabaceae", "urad": "Fabaceae",
    "lentil": "Fabaceae", "masur": "Fabaceae", "mosur": "Fabaceae",
    "chickpea": "Fabaceae", "gram": "Fabaceae", "chola": "Fabaceae", "bengal gram": "Fabaceae",
    "field pea": "Fabaceae", "garden pea": "Fabaceae", "pea": "Fabaceae", "motor": "Fabaceae",
    "khesari": "Fabaceae", "grass pea": "Fabaceae", "lathyrus": "Fabaceae",
    "pigeon pea": "Fabaceae", "pigeonpea": "Fabaceae", "arhar": "Fabaceae", "red gram": "Fabaceae",
    "groundnut": "Fabaceae", "peanut": "Fabaceae", "chinabadam": "Fabaceae", "badam": "Fabaceae",
    "soybean": "Fabaceae", "soya bean": "Fabaceae", "soya": "Fabaceae",
    "country bean": "Fabaceae", "hyacinth bean": "Fabaceae", "lablab": "Fabaceae", "sheem": "Fabaceae", "shim": "Fabaceae",
    "yardlong bean": "Fabaceae", "asparagus bean": "Fabaceae", "borboti": "Fabaceae", "barbati": "Fabaceae",
    "french bean": "Fabaceae", "kidney bean": "Fabaceae", "bush bean": "Fabaceae", "common bean": "Fabaceae",
    "winged bean": "Fabaceae", "faba bean": "Fabaceae", "broad bean": "Fabaceae", "bakla": "Fabaceae",
    "horse gram": "Fabaceae", "kulthi": "Fabaceae", "dhaincha": "Fabaceae", "sesbania": "Fabaceae",
    "sunnhemp": "Fabaceae", "sunn hemp": "Fabaceae", "clover": "Fabaceae", "alfalfa": "Fabaceae",
    "vetch": "Fabaceae", "lupin": "Fabaceae", "fenugreek": "Fabaceae", "methi": "Fabaceae",

    # --- Cucurbitaceae (Gourds, Melons, Squashes) ---
    "ash gourd": "Cucurbitaceae", "wax gourd": "Cucurbitaceae", "white gourd": "Cucurbitaceae", "chal kumra": "Cucurbitaceae",
    "sweet gourd": "Cucurbitaceae", "pumpkin": "Cucurbitaceae", "mishti kumra": "Cucurbitaceae", "squash": "Cucurbitaceae",
    "bottle gourd": "Cucurbitaceae", "calabash": "Cucurbitaceae", "lau": "Cucurbitaceae", "gourd": "Cucurbitaceae",
    "bitter gourd": "Cucurbitaceae", "bitter melon": "Cucurbitaceae", "korola": "Cucurbitaceae", "uchche": "Cucurbitaceae",
    "snake gourd": "Cucurbitaceae", "chichinga": "Cucurbitaceae",
    "ridge gourd": "Cucurbitaceae", "ribbed gourd": "Cucurbitaceae", "jhinga": "Cucurbitaceae",
    "sponge gourd": "Cucurbitaceae", "luffa": "Cucurbitaceae", "dhundul": "Cucurbitaceae",
    "pointed gourd": "Cucurbitaceae", "potol": "Cucurbitaceae", "parwal": "Cucurbitaceae",
    "teasel gourd": "Cucurbitaceae", "spiny gourd": "Cucurbitaceae", "kakrol": "Cucurbitaceae",
    "ivy gourd": "Cucurbitaceae", "telakucha": "Cucurbitaceae", "kundru": "Cucurbitaceae",
    "cucumber": "Cucurbitaceae", "shosha": "Cucurbitaceae", "khira": "Cucurbitaceae", "gherkin": "Cucurbitaceae",
    "watermelon": "Cucurbitaceae", "tormuj": "Cucurbitaceae",
    "muskmelon": "Cucurbitaceae", "cantaloupe": "Cucurbitaceae", "melon": "Cucurbitaceae", "bangi": "Cucurbitaceae", "phuti": "Cucurbitaceae",
    "zucchini": "Cucurbitaceae", "chayote": "Cucurbitaceae", "squash melon": "Cucurbitaceae",

    # --- Malvaceae (Fiber Crops & Okra) ---
    "cotton": "Malvaceae", "tula": "Malvaceae", "upland cotton": "Malvaceae",
    "jute": "Malvaceae", "tossa jute": "Malvaceae", "white jute": "Malvaceae", "deshi jute": "Malvaceae", "pat": "Malvaceae",
    "kenaf": "Malvaceae", "mesta": "Malvaceae", "roselle": "Malvaceae", "chukur": "Malvaceae",
    "okra": "Malvaceae", "ladies finger": "Malvaceae", "lady finger": "Malvaceae", "bhindi": "Malvaceae", "dherosh": "Malvaceae",

    # --- Poaceae (Cereals, Millets, Grasses, Sugarcane) ---
    "t. aman dhan": "Poaceae", "t. aman": "Poaceae", "b. aman": "Poaceae", "aman rice": "Poaceae", "aman": "Poaceae",
    "boro dhan": "Poaceae", "boro rice": "Poaceae", "boro": "Poaceae",
    "aus dhan": "Poaceae", "aus rice": "Poaceae", "t. aus": "Poaceae", "b. aus": "Poaceae", "aus": "Poaceae",
    "rice": "Poaceae", "paddy": "Poaceae", "dhan": "Poaceae",
    "wheat": "Poaceae", "gom": "Poaceae", "durum wheat": "Poaceae",
    "maize": "Poaceae", "corn": "Poaceae", "sweet corn": "Poaceae", "bhutta": "Poaceae",
    "barley": "Poaceae", "job": "Poaceae",
    "oat": "Poaceae", "oats": "Poaceae",
    "rye": "Poaceae", "triticale": "Poaceae",
    "sorghum": "Poaceae", "grain sorghum": "Poaceae", "jowar": "Poaceae",
    "pearl millet": "Poaceae", "bajra": "Poaceae",
    "foxtail millet": "Poaceae", "kaon": "Poaceae",
    "proso millet": "Poaceae", "common millet": "Poaceae", "cheena": "Poaceae",
    "finger millet": "Poaceae", "ragi": "Poaceae", "millet": "Poaceae",
    "sugarcane": "Poaceae", "sugar cane": "Poaceae", "akh": "Poaceae",
    "napier grass": "Poaceae", "para grass": "Poaceae", "bamboo": "Poaceae", "lemongrass": "Poaceae",

    # --- Solanaceae (Nightshades) ---
    "potato": "Solanaceae", "alu": "Solanaceae",
    "brinjal": "Solanaceae", "eggplant": "Solanaceae", "aubergine": "Solanaceae", "begun": "Solanaceae",
    "tomato": "Solanaceae", "cherry tomato": "Solanaceae",
    "chilli": "Solanaceae", "chili": "Solanaceae", "chillies": "Solanaceae", "hot pepper": "Solanaceae",
    "bell pepper": "Solanaceae", "sweet pepper": "Solanaceae", "capsicum": "Solanaceae", "morich": "Solanaceae",
    "tobacco": "Solanaceae", "tamak": "Solanaceae", "physalis": "Solanaceae",

    # --- Brassicaceae (Crucifers / Mustard & Cabbage family) ---
    "mustard": "Brassicaceae", "rapeseed": "Brassicaceae", "sorisha": "Brassicaceae", "toria": "Brassicaceae", "canola": "Brassicaceae",
    "cabbage": "Brassicaceae", "badhakopi": "Brassicaceae",
    "cauliflower": "Brassicaceae", "phulkopi": "Brassicaceae",
    "broccoli": "Brassicaceae",
    "knolkhol": "Brassicaceae", "kohlrabi": "Brassicaceae", "olkopi": "Brassicaceae",
    "radish": "Brassicaceae", "mula": "Brassicaceae",
    "turnip": "Brassicaceae", "shalgom": "Brassicaceae",
    "chinese cabbage": "Brassicaceae", "pak choi": "Brassicaceae", "bok choy": "Brassicaceae", "kale": "Brassicaceae",

    # --- Amaranthaceae / Chenopodiaceae (Leafy Greens, Beets, Quinoa) ---
    "red amaranth": "Amaranthaceae", "lal shak": "Amaranthaceae",
    "stem amaranth": "Amaranthaceae", "data shak": "Amaranthaceae", "amaranth": "Amaranthaceae", "danta": "Amaranthaceae",
    "spinach": "Amaranthaceae", "palong shak": "Amaranthaceae", "palak": "Amaranthaceae",
    "sugar beet": "Amaranthaceae", "beetroot": "Amaranthaceae", "beet": "Amaranthaceae", "chard": "Amaranthaceae",
    "quinoa": "Amaranthaceae", "chenopodium": "Amaranthaceae", "bathua": "Amaranthaceae",

    # --- Apiaceae / Umbelliferae (Carrot, Coriander, Spices) ---
    "coriander": "Apiaceae", "dhonia": "Apiaceae", "cilantro": "Apiaceae",
    "carrot": "Apiaceae", "gajor": "Apiaceae",
    "cumin": "Apiaceae", "jira": "Apiaceae",
    "fennel": "Apiaceae", "mouri": "Apiaceae",
    "dill": "Apiaceae", "shulpha": "Apiaceae",
    "celery": "Apiaceae", "parsley": "Apiaceae", "ajwain": "Apiaceae", "anise": "Apiaceae",

    # --- Amaryllidaceae / Alliaceae (Onion, Garlic) ---
    "onion": "Amaryllidaceae", "peyaj": "Amaryllidaceae", "shallot": "Amaryllidaceae",
    "garlic": "Amaryllidaceae", "roshun": "Amaryllidaceae",
    "leek": "Amaryllidaceae", "chive": "Amaryllidaceae", "spring onion": "Amaryllidaceae",

    # --- Zingiberaceae (Ginger, Turmeric) ---
    "ginger": "Zingiberaceae", "ada": "Zingiberaceae",
    "turmeric": "Zingiberaceae", "holud": "Zingiberaceae",
    "cardamom": "Zingiberaceae", "elachi": "Zingiberaceae",

    # --- Asteraceae / Compositae (Sunflower, Lettuce) ---
    "sunflower": "Asteraceae", "surjomukhi": "Asteraceae",
    "safflower": "Asteraceae", "kusum": "Asteraceae",
    "niger": "Asteraceae", "niger seed": "Asteraceae",
    "lettuce": "Asteraceae", "artichoke": "Asteraceae", "chicory": "Asteraceae", "stevia": "Asteraceae",

    # --- Other Important Crop Families ---
    "sesame": "Pedaliaceae", "sesamum": "Pedaliaceae", "til": "Pedaliaceae",
    "linseed": "Linaceae", "flax": "Linaceae", "tishi": "Linaceae",
    "castor": "Euphorbiaceae", "cassava": "Euphorbiaceae", "tapioca": "Euphorbiaceae", "shimul alu": "Euphorbiaceae",
    "sweet potato": "Convolvulaceae", "mishti alu": "Convolvulaceae",
    "water spinach": "Convolvulaceae", "kangkon": "Convolvulaceae", "kalmi shak": "Convolvulaceae",
    "taro": "Araceae", "arum": "Araceae", "kachu": "Araceae", "mukhi kachu": "Araceae",
    "pani kachu": "Araceae", "ol kachu": "Araceae", "elephant foot yam": "Araceae", "cocoyam": "Araceae",
    "yam": "Dioscoreaceae", "mete alu": "Dioscoreaceae",
    "indian spinach": "Basellaceae", "malabar spinach": "Basellaceae", "pui shak": "Basellaceae",
    "buckwheat": "Polygonaceae", "panchagarh buckwheat": "Polygonaceae",
    "black pepper": "Piperaceae", "betel leaf": "Piperaceae", "paan": "Piperaceae",
    "mint": "Lamiaceae", "pudina": "Lamiaceae", "basil": "Lamiaceae",
    "strawberry": "Rosaceae", "pineapple": "Bromeliaceae", "papaya": "Caricaceae",
    "banana": "Musaceae", "plantain": "Musaceae", "kola": "Musaceae",
    "watermelon": "Cucurbitaceae", "moringa": "Moringaceae", "sajna": "Moringaceae",
}

SYNONYM_FAMILY_MAP: Dict[str, str] = {
    "leguminosae": "Fabaceae",
    "papilionaceae": "Fabaceae",
    "gramineae": "Poaceae",
    "compositae": "Asteraceae",
    "umbelliferae": "Apiaceae",
    "cruciferae": "Brassicaceae",
    "chenopodiaceae": "Amaranthaceae",
    "alliaceae": "Amaryllidaceae",
    "liliaceae": "Amaryllidaceae",
    "tiliaceae": "Malvaceae",
    "bombacaceae": "Malvaceae",
    "sterculiaceae": "Malvaceae",
}

_DYNAMIC_DB_LOADED = False


def _load_local_project_databases(data_dir: str = "data") -> None:
    global _DYNAMIC_DB_LOADED
    if _DYNAMIC_DB_LOADED:
        return
    _DYNAMIC_DB_LOADED = True

    if not os.path.exists(data_dir):
        return

    for csv_path in glob.glob(os.path.join(data_dir, "**", "*.csv"), recursive=True):
        try:
            with open(csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    continue
                name_cols = [c for c in reader.fieldnames if any(k in c.lower() for k in ("crop", "name", "comname", "scientific"))]
                fam_cols = [c for c in reader.fieldnames if "fam" in c.lower()]
                if not name_cols or not fam_cols:
                    continue

                for row in reader:
                    fam_val = (row.get(fam_cols[0]) or "").strip()
                    if not fam_val or fam_val.lower() in ("unknown", "none", "n/a", "null", "na"):
                        continue
                    for nc in name_cols:
                        c_name = (row.get(nc) or "").strip().lower()
                        if c_name and c_name not in BACKUP_FAMILY_DICT:
                            BACKUP_FAMILY_DICT[c_name] = fam_val
        except Exception:
            pass


def standardize_family_name(family: str) -> str:
    clean_fam = family.strip()
    lower_fam = clean_fam.lower()
    if lower_fam in SYNONYM_FAMILY_MAP:
        return SYNONYM_FAMILY_MAP[lower_fam]
    return clean_fam


def resolve_crop_family(crop_name: str, existing_family: str = "Unknown") -> str:
    if existing_family and str(existing_family).strip().lower() not in ("unknown", "none", "n/a", "null", "na", "", "-"):
        return standardize_family_name(str(existing_family))

    if not crop_name:
        return "Unknown"

    _load_local_project_databases()

    raw_lower = str(crop_name).strip().lower()
    no_parens = re.sub(r"\s*\([^)]*\)", "", raw_lower).strip()
    inside_parens_match = re.search(r"\(([^)]+)\)", raw_lower)
    inside_parens = inside_parens_match.group(1).strip() if inside_parens_match else ""

    for candidate in (raw_lower, no_parens, inside_parens):
        if candidate and candidate in BACKUP_FAMILY_DICT:
            return standardize_family_name(BACKUP_FAMILY_DICT[candidate])

    for key in sorted(BACKUP_FAMILY_DICT.keys(), key=len, reverse=True):
        if len(key) >= 3 and re.search(r"\b" + re.escape(key) + r"\b", raw_lower):
            return standardize_family_name(BACKUP_FAMILY_DICT[key])

    return "Unknown"


def enrich_stage3_pools(pools: Any) -> Any:
    if isinstance(pools, dict):
        for season_key, crop_list in pools.items():
            if isinstance(crop_list, list):
                for item in crop_list:
                    _patch_single_crop_item(item)
    elif isinstance(pools, list):
        for item in pools:
            _patch_single_crop_item(item)
    return pools


def _patch_single_crop_item(item: Any) -> None:
    try:
        if isinstance(item, dict):
            name = (
                item.get("crop_name")
                or item.get("name")
                or item.get("crop")
                or ""
            )
            if "botanical_family" in item:
                fam_key = "botanical_family"
            elif "family" in item:
                fam_key = "family"
            elif "Family" in item:
                fam_key = "Family"
            else:
                fam_key = "botanical_family"

            current_fam = item.get(fam_key, "Unknown")
            item[fam_key] = resolve_crop_family(name, current_fam)

        elif hasattr(item, "botanical_family"):
            name = getattr(item, "crop_name", None) or getattr(item, "name", "")
            current_fam = getattr(item, "botanical_family", "Unknown")
            setattr(item, "botanical_family", resolve_crop_family(name, current_fam))

        elif hasattr(item, "family"):
            name = getattr(item, "crop_name", None) or getattr(item, "name", "")
            current_fam = getattr(item, "family", "Unknown")
            setattr(item, "family", resolve_crop_family(name, current_fam))
    except Exception:
        pass
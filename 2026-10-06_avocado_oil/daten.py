from pathlib import Path
import pandas as pd

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-10-06/"
ORDNER = Path(__file__).parent / "data"


def laden(name):
    ORDNER.mkdir(exist_ok=True)
    datei = ORDNER / f"{name}.csv"
    if not datei.exists():
        pd.read_csv(URL + f"{name}.csv").to_csv(datei, index=False)
    return pd.read_csv(datei)


flaschen = laden("avocado_oil_bottles")
lebensmittel = laden("avocado_oil_processed_foods")

flaschen["reinheit"] = pd.Categorical(
    flaschen["purity_result"].map({"pure": "rein", "suspected": "verdächtig", "adulterated": "gepanscht"}),
    categories=["rein", "verdächtig", "gepanscht"],
)
flaschen["fremdoel"] = flaschen["adulterant"].map(
    {"soybean oil": "Sojaöl", "sunflower/safflower oil": "Sonnenblumen-/Distelöl"}
).fillna("keins")

echtheit = lebensmittel.groupby(["category", "oil_type"], as_index=False).agg(
    anteil=("authentic", "mean"), proben=("authentic", "size")
)
echtheit["anteil"] = echtheit["anteil"] * 100
echtheit["kategorie"] = echtheit["category"].map({"chips": "Chips", "mayonnaise": "Mayonnaise", "salad_dressing": "Salatdressing"})
echtheit["oel"] = echtheit["oil_type"].map({"avocado": "Avocadoöl", "olive": "Olivenöl"})

preis = flaschen[["sample_code", "grade_labeled", "reinheit", "cost_per_fl_oz"]]
marker = flaschen[["sample_code", "reinheit", "fremdoel", "c16_1_palmitoleic_pct", "c18_2_linoleic_pct"]]

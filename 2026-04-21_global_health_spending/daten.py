from pathlib import Path
import pandas as pd

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-04-21/"
ORDNER = Path(__file__).parent / "data"


def laden(name):
    ORDNER.mkdir(exist_ok=True)
    datei = ORDNER / f"{name}.csv"
    if not datei.exists():
        pd.read_csv(URL + f"{name}.csv").to_csv(datei, index=False)
    return pd.read_csv(datei)


health_spending = laden("health_spending")
financing_schemes = laden("financing_schemes")
spending_purpose = laden("spending_purpose")

# "value" enthält Prozentwerte und Dollarbeträge hier nur Prozent
quellen_codes = {"gghed_che": "Staat", "pvtd_che": "Privat", "ext_che": "Extern"}
quellen = health_spending[health_spending["indicator_code"].isin(quellen_codes)]
quellen = quellen.pivot_table(index=["country_name", "year"], columns="indicator_code", values="value")
quellen = quellen.rename(columns=quellen_codes).reset_index()
quellen["Extern"] = quellen["Extern"].fillna(0)  # fehlende Zeile = keine externen Gelder
quellen = quellen.melt(id_vars=["country_name", "year"], var_name="quelle", value_name="anteil")

oop = financing_schemes[financing_schemes["indicator_code"] == "hf3_che"]
oop = oop[["country_name", "year", "value"]].rename(columns={"value": "oop"})

# Prävention gibt es erst ab 2016, nur Länder mit allen 8 Jahren
prev = spending_purpose[spending_purpose["indicator_code"] == "hc6_che"]
jahre = prev.groupby("country_name")["year"].nunique()
prev = prev[prev["country_name"].isin(jahre[jahre == 8].index)]

ranking = oop[oop["year"] == 2023].nlargest(15, "oop")
finanzierung = quellen.groupby(["year", "quelle"], as_index=False)["anteil"].median()
praevention = prev.groupby("year", as_index=False).agg(anteil=("value", "median"))
praevention["corona"] = praevention["year"].between(2020, 2022)
praevention_laender = prev["country_name"].nunique()

from pathlib import Path
import pandas as pd

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-10-13/"
ORDNER = Path(__file__).parent / "data"


def laden(name):
    ORDNER.mkdir(exist_ok=True)
    datei = ORDNER / f"{name}.csv"
    if not datei.exists():
        pd.read_csv(URL + f"{name}.csv").to_csv(datei, index=False)
    return pd.read_csv(datei)


froesche = laden("frogs_and_toads_amphibiaweb")

# isocc: Ländercodes des natürlichen Verbreitungsgebiets, durch Komma getrennt
laender = froesche["isocc"].str.strip(",").str.split(",")
anzahl_laender = laender.str.len()

NAMEN = {
    "BR": "Brasilien", "CO": "Kolumbien", "EC": "Ecuador", "PE": "Peru", "CN": "China",
    "MG": "Madagaskar", "PG": "Papua-Neuguinea", "IN": "Indien", "ID": "Indonesien",
    "VE": "Venezuela", "MY": "Malaysia", "VN": "Vietnam", "MX": "Mexiko",
    "BO": "Bolivien", "AU": "Australien",
}

familien = froesche["family"].value_counts().head(10).rename_axis("familie").reset_index(name="arten")

pro_land = froesche.assign(land=laender, nur_hier=anzahl_laender == 1).explode("land")
top_laender = pro_land.groupby("land").agg(arten=("amphib_id", "size"), nur_hier=("nur_hier", "sum"))
top_laender = top_laender.nlargest(15, "arten").reset_index()
top_laender["name"] = top_laender["land"].map(NAMEN)
top_laender["auch_anderswo"] = top_laender["arten"] - top_laender["nur_hier"]
laender_lang = top_laender.melt(id_vars=["name", "arten"], value_vars=["nur_hier", "auch_anderswo"],
                                var_name="vorkommen", value_name="anzahl")
laender_lang["vorkommen"] = laender_lang["vorkommen"].map({"nur_hier": "nur hier", "auch_anderswo": "auch anderswo"})

gruppen = pd.cut(anzahl_laender, bins=[0, 1, 2, 3, 4, 1000], labels=["1", "2", "3", "4", "5+"])
verbreitung = gruppen.value_counts(sort=False).rename_axis("laender").reset_index(name="arten")

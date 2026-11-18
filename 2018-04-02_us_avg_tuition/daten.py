from pathlib import Path
import pandas as pd

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2018/2018-04-02/"
ORDNER = Path(__file__).parent / "data"


def laden(name):
    ORDNER.mkdir(exist_ok=True)
    datei = ORDNER / f"{name}.csv"
    if not datei.exists():
        pd.read_excel(URL + f"{name}.xlsx").to_csv(datei, index=False)
    return pd.read_csv(datei)


us_avg_tuition = laden("us_avg_tuition")

# ein Spaltenname hat Leerzeichen: "  2007-08 "
us_avg_tuition.columns = us_avg_tuition.columns.str.strip()

# vom breiten ins lange Format: eine Zeile pro Staat und Studienjahr
gebuehren = us_avg_tuition.melt(id_vars="State", var_name="jahr", value_name="gebuehr")
gebuehren = gebuehren.rename(columns={"State": "staat"})
gebuehren["jahr"] = gebuehren["jahr"].str[:4].astype(int)  # "2004-05" -> 2004

anstieg = us_avg_tuition[["State"]].rename(columns={"State": "staat"})
anstieg["anstieg"] = (us_avg_tuition["2015-16"] / us_avg_tuition["2004-05"] - 1) * 100
anstieg["gruppe"] = "übrige"
anstieg.loc[anstieg["anstieg"].rank(ascending=False) <= 5, "gruppe"] = "stärkster Anstieg"
anstieg.loc[anstieg["anstieg"].rank() <= 5, "gruppe"] = "schwächster Anstieg"

entwicklung = gebuehren.groupby("jahr", as_index=False).agg(gebuehr=("gebuehr", "median"))

pro_jahr = entwicklung.copy()
pro_jahr["anstieg"] = pro_jahr["gebuehr"].pct_change() * 100
pro_jahr = pro_jahr.dropna()
pro_jahr["finanzkrise"] = pro_jahr["jahr"].between(2009, 2010)

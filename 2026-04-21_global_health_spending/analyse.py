from pathlib import Path

import daten
import plots

print("Größe der Tabellen:")
print("health_spending:  ", daten.health_spending.shape)
print("financing_schemes:", daten.financing_schemes.shape)
print("spending_purpose: ", daten.spending_purpose.shape)

tabellen = {
    "health_spending": daten.health_spending,
    "financing_schemes": daten.financing_schemes,
    "spending_purpose": daten.spending_purpose,
}
for name, tabelle in tabellen.items():
    print(f"\n{name}: Spalten, Datentypen und erste Zeilen")
    print(tabelle.dtypes)
    print(tabelle.head())

print("\nFehlende Werte:", daten.health_spending.isna().sum().sum())

print("\nWelche Indikatoren gibt es in health_spending?")
print(daten.health_spending.groupby(["indicator_code", "unit"]).size())

print("\nLänder pro Jahr (spending_purpose erst ab 2016):")
print(daten.spending_purpose.groupby("year")["country_name"].nunique())

print("\nFrage 1: Höchste Selbstzahler-Anteile 2023")
print(daten.ranking.head(10))
deutschland = daten.oop[(daten.oop["year"] == 2023) & (daten.oop["country_name"] == "Germany")]["oop"].values[0]
print(f"Deutschland zum Vergleich: {deutschland:.1f} %")

print("\nFrage 2: Median-Anteile über alle Länder")
median = daten.finanzierung.pivot(index="year", columns="quelle", values="anteil")
print(median.loc[[2000, 2010, 2019, 2020, 2023]].round(1))

print("\nFrage 3: Anteil Prävention (Median)")
print(daten.praevention.round(1))

Path("grafiken").mkdir(exist_ok=True)
plots.selbstzahler().save("grafiken/01_selbstzahler.png", dpi=150, verbose=False)
plots.finanzierung().save("grafiken/02_finanzierung.png", dpi=150, verbose=False)
plots.praevention().save("grafiken/03_praevention.png", dpi=150, verbose=False)
print("\nGrafiken liegen im Ordner grafiken/")

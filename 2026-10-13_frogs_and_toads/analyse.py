from pathlib import Path

import daten
import plots

print("Größe der Tabelle:", daten.froesche.shape)
print("\nSpalten, Datentypen und erste Zeilen:")
print(daten.froesche.dtypes)
print(daten.froesche.head())

print("\nAnteil fehlender Werte pro Spalte:")
print(daten.froesche.isna().mean().round(2).sort_values())

print("\nArten ohne Länderangabe:", daten.froesche["isocc"].isna().sum())
print("Familien:", daten.froesche["family"].nunique(), "· Gattungen:", daten.froesche["genus"].nunique())

print("\nFrage 1: Artenreichste Familien")
print(daten.familien)

print("\nFrage 2: Länder mit den meisten Arten")
print(daten.top_laender[["name", "arten", "nur_hier"]])

print("\nFrage 3: Arten nach Anzahl Länder")
print(daten.verbreitung)
print(f"Nur in einem Land: {(daten.anzahl_laender.dropna() == 1).mean() * 100:.0f} %")

Path("grafiken").mkdir(exist_ok=True)
plots.familien().save("grafiken/01_familien.png", dpi=150, verbose=False)
plots.laender().save("grafiken/02_laender.png", dpi=150, verbose=False)
plots.verbreitung().save("grafiken/03_verbreitung.png", dpi=150, verbose=False)
print("\nGrafiken liegen im Ordner grafiken/")

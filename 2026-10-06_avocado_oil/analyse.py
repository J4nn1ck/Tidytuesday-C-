from pathlib import Path

import daten
import plots

print("Größe der Tabellen:")
print("Flaschen:    ", daten.flaschen.shape)
print("Lebensmittel:", daten.lebensmittel.shape)

for name, tabelle in {"Flaschen": daten.flaschen, "Lebensmittel": daten.lebensmittel}.items():
    print(f"\n{name}: Spalten, Datentypen und erste Zeilen")
    print(tabelle.dtypes)
    print(tabelle.head())

print("\nFehlende Werte pro Spalte (Flaschen):")
print(daten.flaschen.isna().sum()[lambda s: s > 0])

print("\nReinheit nach Angabe auf dem Etikett:")
print(daten.flaschen.groupby(["grade_labeled", "reinheit"]).size().unstack(fill_value=0))
print("oxidiert:", daten.flaschen["oxidized"].sum(), "von", len(daten.flaschen))

print("\nFrage 1: Anteil echter Lebensmittel")
print(daten.echtheit[["kategorie", "oel", "proben", "anteil"]].round(1))

print("\nFrage 2: Preis pro fl oz nach Reinheit (Median)")
print(daten.preis.groupby("reinheit", observed=True)["cost_per_fl_oz"].median())

print("\nFrage 3: Fettsäuren nach Reinheit (Mittelwert)")
print(daten.marker.groupby("reinheit", observed=True)[["c16_1_palmitoleic_pct", "c18_2_linoleic_pct"]].mean().round(1))

Path("grafiken").mkdir(exist_ok=True)
plots.lebensmittel().save("grafiken/01_lebensmittel.png", dpi=150, verbose=False)
plots.preis().save("grafiken/02_preis.png", dpi=150, verbose=False)
plots.marker().save("grafiken/03_marker.png", dpi=150, verbose=False)
print("\nGrafiken liegen im Ordner grafiken/")

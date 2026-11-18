from pathlib import Path

import daten
import plots

print("Größe der Tabelle:", daten.us_avg_tuition.shape)

print("\nSpalten, Datentypen und erste Zeilen:")
print(daten.us_avg_tuition.dtypes)
print(daten.us_avg_tuition.head())

print("\nFehlende Werte:", daten.us_avg_tuition.isna().sum().sum())

print("\nNach der Aufbereitung (langes Format):", daten.gebuehren.shape)
print(daten.gebuehren.head())

print("\nFrage 1: Anstieg 2004/05 bis 2015/16 in %")
print("stärkster Anstieg:")
print(daten.anstieg.nlargest(5, "anstieg")[["staat", "anstieg"]].round(1))
print("schwächster Anstieg:")
print(daten.anstieg.nsmallest(5, "anstieg")[["staat", "anstieg"]].round(1))

print("\nFrage 2: Gebühr im typischen Bundesstaat (Median) in $")
print(daten.entwicklung.round(0))

print("\nFrage 3: Anstieg zum Vorjahr in %")
print(daten.pro_jahr[["jahr", "anstieg"]].round(1))

Path("grafiken").mkdir(exist_ok=True)
plots.anstieg().save("grafiken/01_anstieg.png", dpi=150, verbose=False)
plots.entwicklung().save("grafiken/02_entwicklung.png", dpi=150, verbose=False)
plots.pro_jahr().save("grafiken/03_pro_jahr.png", dpi=150, verbose=False)
print("\nGrafiken liegen im Ordner grafiken/")

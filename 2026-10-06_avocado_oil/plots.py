from plotnine import (
    aes, geom_col, geom_jitter, geom_point, ggplot, labs, position_dodge,
    position_jitter, scale_color_manual, scale_fill_manual, theme_minimal,
)

import daten

BLAU, ORANGE, GRUEN, ROT = "#2a78d6", "#eb6834", "#1baf7a", "#c7303b"
OELE = {"Avocadoöl": GRUEN, "Olivenöl": BLAU}
REINHEIT = {"rein": GRUEN, "verdächtig": ORANGE, "gepanscht": ROT}
QUELLE = "Quelle: UC Davis · #TidyTuesday 2026-10-06"
TITEL = {
    "lebensmittel": "Anteil echter Produkte nach Kategorie",
    "preis": "Preis von Avocadoöl in Flaschen nach Reinheit",
    "marker": "Fettsäuren verraten gepanschtes Öl",
}


def lebensmittel():
    return (
        ggplot(daten.echtheit, aes("kategorie", "anteil", fill="oel"))
        + geom_col(position=position_dodge())
        + scale_fill_manual(values=OELE)
        + labs(x="", y="echt in %", fill="", title=TITEL["lebensmittel"], caption=QUELLE)
        + theme_minimal()
    )


def preis():
    return (
        ggplot(daten.preis, aes("reinheit", "cost_per_fl_oz", color="reinheit"))
        + geom_jitter(position=position_jitter(width=0.15, height=0, random_state=1), size=3)
        + scale_color_manual(values=REINHEIT)
        + labs(x="", y="Preis in $ pro fl oz", color="", title=TITEL["preis"], caption=QUELLE)
        + theme_minimal()
    )


def marker():
    return (
        ggplot(daten.marker, aes("c18_2_linoleic_pct", "c16_1_palmitoleic_pct", color="reinheit"))
        + geom_point(size=3)
        + scale_color_manual(values=REINHEIT)
        + labs(x="Linolsäure in %", y="Palmitoleinsäure in %", color="",
               title=TITEL["marker"], caption=QUELLE)
        + theme_minimal()
    )

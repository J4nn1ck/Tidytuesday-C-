from plotnine import (
    aes, coord_flip, geom_col, geom_line, ggplot, labs,
    scale_color_manual, scale_fill_manual, theme, theme_minimal,
)

import daten

BLAU, ORANGE, GRUEN = "#2a78d6", "#eb6834", "#1baf7a"
FARBEN = {"Staat": BLAU, "Privat": ORANGE, "Extern": GRUEN}
QUELLE = "Quelle: WHO GHED · #TidyTuesday 2026-04-21"
TITEL = {
    "selbstzahler": "Höchste Selbstzahler-Anteile 2023",
    "finanzierung": "Wie finanziert sich ein typisches Land? (Median)",
    "praevention": f"Ausgaben für Prävention – Corona-Jahre in Orange ({daten.praevention_laender} Länder)",
}


def selbstzahler():
    return (
        ggplot(daten.ranking, aes("reorder(country_name, oop)", "oop"))
        + geom_col(fill=BLAU)
        + coord_flip()
        + labs(x="", y="Selbstzahlungen in % der Gesundheitsausgaben",
               title=TITEL["selbstzahler"], caption=QUELLE)
        + theme_minimal()
    )


def finanzierung():
    return (
        ggplot(daten.finanzierung, aes("year", "anteil", color="quelle"))
        + geom_line(size=1)
        + scale_color_manual(values=FARBEN)
        + labs(x="", y="Anteil in %", color="", title=TITEL["finanzierung"], caption=QUELLE)
        + theme_minimal()
    )


def praevention():
    return (
        ggplot(daten.praevention, aes("year", "anteil", fill="corona"))
        + geom_col()
        + scale_fill_manual(values={False: BLAU, True: ORANGE})
        + labs(x="", y="Anteil in % (Median)", title=TITEL["praevention"], caption=QUELLE)
        + theme_minimal()
        + theme(legend_position="none")
    )

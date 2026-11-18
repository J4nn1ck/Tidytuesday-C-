import pandas as pd
from plotnine import aes, coord_flip, geom_col, ggplot, labs, position_stack, scale_fill_manual, theme_minimal

import daten

BLAU, ORANGE = "#2a78d6", "#eb6834"
VORKOMMEN = {"nur hier": ORANGE, "auch anderswo": BLAU}
QUELLE = "Quelle: AmphibiaWeb · #TidyTuesday 2026-10-13"
TITEL = {
    "laender": "Länder mit den meisten Froscharten – Orange: kommt nur dort vor",
    "familien": "Die 10 artenreichsten Froschfamilien",
    "verbreitung": "In wie vielen Ländern kommt eine Art vor?",
}


def laender():
    df = daten.laender_lang.copy()
    df["vorkommen"] = pd.Categorical(df["vorkommen"], categories=list(VORKOMMEN))  # "nur hier" zuerst
    return (
        ggplot(df, aes("reorder(name, arten)", "anzahl", fill="vorkommen"))
        + geom_col(position=position_stack(reverse=True))
        + coord_flip()
        + scale_fill_manual(values=VORKOMMEN)
        + labs(x="", y="Anzahl Arten", fill="", title=TITEL["laender"], caption=QUELLE)
        + theme_minimal()
    )


def familien():
    return (
        ggplot(daten.familien, aes("reorder(familie, arten)", "arten"))
        + geom_col(fill=BLAU)
        + coord_flip()
        + labs(x="", y="Anzahl Arten", title=TITEL["familien"], caption=QUELLE)
        + theme_minimal()
    )


def verbreitung():
    return (
        ggplot(daten.verbreitung, aes("laender", "arten"))
        + geom_col(fill=BLAU)
        + labs(x="Anzahl Länder", y="Anzahl Arten", title=TITEL["verbreitung"], caption=QUELLE)
        + theme_minimal()
    )

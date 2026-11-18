from plotnine import (
    aes, coord_flip, geom_col, geom_line, geom_point, ggplot, labs,
    scale_fill_manual, theme, theme_minimal,
)

import daten

BLAU, ORANGE, GRUEN, GRAU = "#2a78d6", "#eb6834", "#1baf7a", "#b8bcc2"
GRUPPEN = {"stärkster Anstieg": ORANGE, "schwächster Anstieg": GRUEN, "übrige": GRAU}
QUELLE = "Quelle: onlinembapage.com · #TidyTuesday 2018-04-02"
TITEL = {
    "anstieg": "Anstieg der Studiengebühren 2004/05 bis 2015/16 je Bundesstaat",
    "entwicklung": "Studiengebühren im typischen Bundesstaat (Median)",
    "pro_jahr": "Anstieg zum Vorjahr – Orange: Jahre nach der Finanzkrise",
}


def anstieg():
    return (
        ggplot(daten.anstieg, aes("reorder(staat, anstieg)", "anstieg", fill="gruppe"))
        + geom_col()
        + coord_flip()
        + scale_fill_manual(values=GRUPPEN, breaks=list(GRUPPEN))
        + labs(x="", y="Anstieg in %", fill="", title=TITEL["anstieg"], caption=QUELLE)
        + theme_minimal()
        + theme(figure_size=(7, 10))
    )


def entwicklung():
    return (
        ggplot(daten.entwicklung, aes("jahr", "gebuehr"))
        + geom_line(color=BLAU, size=1)
        + geom_point(color=BLAU)
        + labs(x="Studienjahr ab", y="Gebühr in $ pro Jahr", title=TITEL["entwicklung"], caption=QUELLE)
        + theme_minimal()
    )


def pro_jahr():
    return (
        ggplot(daten.pro_jahr, aes("jahr", "anstieg", fill="finanzkrise"))
        + geom_col()
        + scale_fill_manual(values={False: BLAU, True: ORANGE})
        + labs(x="Studienjahr ab", y="Anstieg zum Vorjahr in %", title=TITEL["pro_jahr"], caption=QUELLE)
        + theme_minimal()
        + theme(legend_position="none")
    )

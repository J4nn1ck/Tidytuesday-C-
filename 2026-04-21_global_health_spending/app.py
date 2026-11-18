import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_plotly

import daten
from plots import BLAU, FARBEN, ORANGE, QUELLE, TITEL


def karte(id):
    return ui.card(ui.card_header(TITEL[id]), output_widget(id), full_screen=True)


app_ui = ui.page_fillable(
    ui.h3("Globale Gesundheitsausgaben"),
    ui.layout_columns(
        karte("selbstzahler"),
        ui.layout_column_wrap(karte("finanzierung"), karte("praevention"), width=1),
    ),
    ui.p(QUELLE, class_="text-muted small"),
    title="Gesundheitsausgaben",
)


def server(input, output, session):

    @render_plotly
    def selbstzahler():
        fig = px.bar(daten.ranking, x="oop", y="country_name", orientation="h",
                     labels={"oop": "Selbstzahlungen in % der Gesundheitsausgaben", "country_name": ""},
                     color_discrete_sequence=[BLAU], template="plotly_white")
        return fig.update_yaxes(categoryorder="total ascending")

    @render_plotly
    def finanzierung():
        return px.line(daten.finanzierung, x="year", y="anteil", color="quelle", markers=True,
                       color_discrete_map=FARBEN, template="plotly_white",
                       labels={"year": "", "anteil": "Anteil in %", "quelle": ""})

    @render_plotly
    def praevention():
        fig = px.bar(daten.praevention, x="year", y="anteil", template="plotly_white",
                     labels={"year": "", "anteil": "Anteil in % (Median)"})
        return fig.update_traces(marker_color=daten.praevention["corona"].map({True: ORANGE, False: BLAU}))


app = App(app_ui, server)

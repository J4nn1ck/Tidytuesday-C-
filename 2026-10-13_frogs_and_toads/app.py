import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_plotly

import daten
from plots import BLAU, QUELLE, TITEL, VORKOMMEN


def karte(id):
    return ui.card(ui.card_header(TITEL[id]), output_widget(id), full_screen=True)


app_ui = ui.page_fillable(
    ui.h3("Frösche und Kröten weltweit"),
    ui.layout_columns(
        karte("laender"),
        ui.layout_column_wrap(karte("familien"), karte("verbreitung"), width=1),
    ),
    ui.p(QUELLE, class_="text-muted small"),
    title="Frösche und Kröten",
)


def server(input, output, session):

    @render_plotly
    def laender():
        fig = px.bar(daten.laender_lang, x="anzahl", y="name", color="vorkommen", orientation="h",
                     color_discrete_map=VORKOMMEN, hover_data=["arten"], template="plotly_white",
                     labels={"anzahl": "Anzahl Arten", "name": "", "vorkommen": "", "arten": "gesamt"})
        return fig.update_yaxes(categoryorder="total ascending")

    @render_plotly
    def familien():
        fig = px.bar(daten.familien, x="arten", y="familie", orientation="h",
                     color_discrete_sequence=[BLAU], template="plotly_white",
                     labels={"arten": "Anzahl Arten", "familie": ""})
        return fig.update_yaxes(categoryorder="total ascending")

    @render_plotly
    def verbreitung():
        return px.bar(daten.verbreitung, x="laender", y="arten", color_discrete_sequence=[BLAU],
                      template="plotly_white", labels={"laender": "Anzahl Länder", "arten": "Anzahl Arten"})


app = App(app_ui, server)

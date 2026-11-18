import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_plotly

import daten
from plots import BLAU, GRUPPEN, ORANGE, QUELLE, TITEL


def karte(id):
    return ui.card(ui.card_header(TITEL[id]), output_widget(id), full_screen=True)


app_ui = ui.page_fillable(
    ui.h3("Studiengebühren in den USA"),
    ui.layout_columns(
        karte("anstieg"),
        ui.layout_column_wrap(karte("entwicklung"), karte("pro_jahr"), width=1),
    ),
    ui.p(QUELLE, class_="text-muted small"),
    title="Studiengebühren",
)


def server(input, output, session):

    @render_plotly
    def anstieg():
        fig = px.bar(daten.anstieg, x="anstieg", y="staat", color="gruppe", orientation="h",
                     color_discrete_map=GRUPPEN, category_orders={"gruppe": list(GRUPPEN)},
                     template="plotly_white", labels={"anstieg": "Anstieg in %", "staat": "", "gruppe": ""})
        return fig.update_yaxes(categoryorder="total ascending")

    @render_plotly
    def entwicklung():
        return px.line(daten.entwicklung, x="jahr", y="gebuehr", markers=True,
                       color_discrete_sequence=[BLAU], template="plotly_white",
                       labels={"jahr": "Studienjahr ab", "gebuehr": "Gebühr in $ pro Jahr"})

    @render_plotly
    def pro_jahr():
        fig = px.bar(daten.pro_jahr, x="jahr", y="anstieg", template="plotly_white",
                     labels={"jahr": "Studienjahr ab", "anstieg": "Anstieg zum Vorjahr in %"})
        return fig.update_traces(marker_color=daten.pro_jahr["finanzkrise"].map({True: ORANGE, False: BLAU}))


app = App(app_ui, server)

import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_plotly

import daten
from plots import OELE, QUELLE, REINHEIT, TITEL


def karte(id):
    return ui.card(ui.card_header(TITEL[id]), output_widget(id), full_screen=True)


app_ui = ui.page_fillable(
    ui.h3("Echtheit von Avocadoöl"),
    ui.layout_columns(
        karte("marker"),
        ui.layout_column_wrap(karte("lebensmittel"), karte("preis"), width=1),
    ),
    ui.p(QUELLE, class_="text-muted small"),
    title="Avocadoöl",
)


def server(input, output, session):

    @render_plotly
    def marker():
        return px.scatter(daten.marker, x="c18_2_linoleic_pct", y="c16_1_palmitoleic_pct",
                          color="reinheit", color_discrete_map=REINHEIT, hover_name="sample_code",
                          hover_data=["fremdoel"], category_orders={"reinheit": list(REINHEIT)},
                          template="plotly_white",
                          labels={"c18_2_linoleic_pct": "Linolsäure in %",
                                  "c16_1_palmitoleic_pct": "Palmitoleinsäure in %", "reinheit": "", "fremdoel": "Fremdöl"})

    @render_plotly
    def lebensmittel():
        return px.bar(daten.echtheit, x="kategorie", y="anteil", color="oel", barmode="group",
                      color_discrete_map=OELE, hover_data=["proben"], template="plotly_white",
                      labels={"kategorie": "", "anteil": "echt in %", "oel": "", "proben": "Proben"})

    @render_plotly
    def preis():
        return px.strip(daten.preis, x="reinheit", y="cost_per_fl_oz", color="reinheit",
                        color_discrete_map=REINHEIT, hover_name="sample_code",
                        hover_data=["grade_labeled"], category_orders={"reinheit": list(REINHEIT)},
                        template="plotly_white",
                        labels={"reinheit": "", "cost_per_fl_oz": "Preis in $ pro fl oz"})


app = App(app_ui, server)

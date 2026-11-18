import importlib.util
import sys
from pathlib import Path

from shiny import App, ui
from starlette.applications import Starlette
from starlette.routing import Mount

HAUPTORDNER = Path(__file__).parent


def laden(ordner):
    # jedes Dashboard hat eigene Module "daten" und "plots", deshalb nacheinander laden
    pfad = HAUPTORDNER / ordner
    sys.path.insert(0, str(pfad))
    spec = importlib.util.spec_from_file_location(f"app_{ordner}", pfad / "app.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    sys.path.remove(str(pfad))
    del sys.modules["daten"], sys.modules["plots"]
    return modul.app


def reiter(titel, adresse):
    # data-src statt src: das Dashboard lädt erst, wenn der Reiter geöffnet wird
    return ui.nav_panel(titel, ui.tags.iframe(data_src=adresse, style="width:100%; height:100%; border:none;"))


# kopiert data-src nach src, sobald ein Reiter sichtbar ist (sonst werden Legenden abgeschnitten)
NACHLADEN = """
function nachladen() {
  document.querySelectorAll("iframe").forEach(f => {
    if (f.offsetParent !== null && !f.src) f.src = f.dataset.src;
  });
}
document.addEventListener("DOMContentLoaded", nachladen);
document.addEventListener("shown.bs.tab", nachladen);
"""

startseite = App(
    ui.page_navbar(
        reiter("Gesundheitsausgaben", "gesundheit/"),
        reiter("Avocadoöl", "avocado/"),
        reiter("Frösche und Kröten", "froesche/"),
        reiter("Studiengebühren", "studiengebuehren/"),
        header=ui.tags.script(NACHLADEN),
        title="TidyTuesday",
        fillable=True,
    ),
    None,
)

app = Starlette(routes=[
    Mount("/gesundheit", app=laden("2026-04-21_global_health_spending")),
    Mount("/avocado", app=laden("2026-10-06_avocado_oil")),
    Mount("/froesche", app=laden("2026-10-13_frogs_and_toads")),
    Mount("/studiengebuehren", app=laden("2018-04-02_us_avg_tuition")),
    Mount("/", app=startseite),  # zuletzt, sonst fängt "/" alle Adressen ab
])

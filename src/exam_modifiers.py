import numpy as np
import pandas as pd


def berechne_durchschnittsnote(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """
        Berechnet die Durchschnittsnote für jedes Modul je Semester.

    Args:
        klausurdaten (pd.DataFrame): Ein DataFrame mit Modulname- Nummer, Semester,
        Teilnehmer und Noten (1 bis 5) als Spalten. Noten in den Spalten 3 bis 8.

    Returns:
        klausurdaten_durchschnitt (pd.DataFrame): klausurdaten mit neuer Spalte
        Durchschnittsnote.
    """
    
    klausurdaten_durchschnitt = klausurdaten.copy()
    klausurdaten_durchschnitt["Durchschnittsnote"] = klausurdaten_durchschnitt.iloc[:, 3:9].apply(lambda x: np.sum(x.iloc[1:6] * np.arange(1,6))/x.iloc[0] if x.iloc[0] != 0 else 0, axis=1)
    klausurdaten_durchschnitt["Durchschnittsnote"] = np.round(klausurdaten_durchschnitt["Durchschnittsnote"], 4)

    return klausurdaten_durchschnitt



def fuege_studiengang_hinzu(klausurdaten: pd.DataFrame, studiengaenge: pd.DataFrame) -> pd.DataFrame:
    
    # Einige ältere Module sind nicht mehr in den Prüfungsordnungen vermerkt
    # Vermutung: Bachelormodule ab 31... und Mastermodule ab 32...
    # wenn unter 32... dann bachelor, sonst Master
    klausurdaten_plus_studiengaenge = pd.merge(klausurdaten, studiengaenge, how="left", on="Modulnummer")
    
    leere_studiengaenge = klausurdaten_plus_studiengaenge[klausurdaten_plus_studiengaenge["Studiengang"].isnull()].index
    klausurdaten_plus_studiengaenge.loc[leere_studiengaenge, "Studiengang"] = klausurdaten_plus_studiengaenge["Modulnummer"].map(lambda x: "Bachelor" if x < 32000 else "Master")
    return klausurdaten_plus_studiengaenge

    
def replace_semester(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    klausurdaten_replaced = klausurdaten.copy()
    klausurdaten_replaced["Semester"] = klausurdaten_replaced["Semester"].str.replace("Sommersemester", "SS").str.replace("Wintersemester", "WS")
    
    return klausurdaten_replaced
    
def time_proxy(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    klausurdaten_time = klausurdaten.copy()
    
    klausurdaten_time["Zeitpunkt"] = list(map(lambda x: pd.to_datetime(f"01.09.{x[3:]}", format="%d.%m.%Y") if x[:2] \
    == "SS" else pd.to_datetime(f"01.03.{int(x[3:])+1}", format="%d.%m.%Y"), klausurdaten_time["Semester"]))
    
    return klausurdaten_time
    
def summarize_vor_nachklausur(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    klausurdaten_copy = klausurdaten.copy()
    
    klausurdaten_summarized = klausurdaten_copy.groupby(["Modulname", "Modulnummer", "Semester"]) \
    .agg({"Teilnehmer": "sum", "sehr gut": "sum", "gut": "sum", "befriedigend": "sum", "ausreichend": "sum", "nicht ausreichend": "sum", "Zeitpunkt": "max"}) \
    .reset_index()
    
    return klausurdaten_summarized
    
def sort_by_module(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    klausurdaten_copy = klausurdaten.copy()
    return klausurdaten_copy.sort_values(by=["Zeitpunkt", "Semester"], ascending = [False, True])
    
def expand_wintersemester(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    klausurdaten_replaced = klausurdaten.copy()
    klausurdaten_replaced.loc[klausurdaten_replaced["Semester"].str.startswith("WS"), "Semester"] \
    = list(map(lambda x: f"{x}/{int(x[5:])+1}", klausurdaten_replaced[klausurdaten_replaced["Semester"].str.startswith("WS")]["Semester"]))
    
    return klausurdaten_replaced
    
def concatenate_module(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    klausurdaten_concate = klausurdaten.copy()
    klausurdaten_concate["Modul"] = klausurdaten_concate["Modulnummer"].astype("str").str.cat(klausurdaten_concate["Modulname"], sep=" - ")
    
    return klausurdaten_concate
import numpy as np
import pandas as pd


def berechne_durchschnittsnote(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """Berechnet die Durchschnittsnote für jedes Modul je Semester.

    Args:
    klausurdaten (pd.DataFrame): Ein DataFrame mit Modulname- Nummer, Semester,
    Teilnehmer und Noten (1 bis 5) als Spalten. Noten in den Spalten 3 bis 8.

    Returns:
    klausurdaten mit neuer Spalte Durchschnittsnot
        
    Raises:
    
    Examples:
    
    Note:
    """
    
    klausurdaten_durchschnitt = klausurdaten.copy()
    klausurdaten_durchschnitt["Durchschnittsnote"] = klausurdaten_durchschnitt.iloc[:, 3:9].apply(lambda x: np.sum(x.iloc[1:6] * np.arange(1,6))/x.iloc[0] if x.iloc[0] != 0 else 0, axis=1)
    klausurdaten_durchschnitt["Durchschnittsnote"] = np.round(klausurdaten_durchschnitt["Durchschnittsnote"], 4)

    return klausurdaten_durchschnitt



def fuege_studiengang_hinzu(klausurdaten: pd.DataFrame, studiengaenge: pd.DataFrame) -> pd.DataFrame:
    """Joined Bachelor/Master an die Klausurdaten
    
    Args:
    klausurdaten: Daten über Klausuren
    studiengaenge: Daten mit Modulnummer und Bachelor/Master-Attribut
    
    Returns:
    Daten über Klausuren mit Bachelor/Master-Attribut
    
    Raises:
    
    
    Examples:
    fuege_studiengang_hinzu(klausurdaten, studiengaenge)
    
    Note:
    Einige ältere Module sind nicht mehr in den Prüfungsordnungen vermerkt.
    Vermutung: Bachelormodule ab 31... und Mastermodule ab 32...
    """
    
    klausurdaten_plus_studiengaenge = pd.merge(klausurdaten, studiengaenge, how="left", on="Modulnummer")
    
    leere_studiengaenge = klausurdaten_plus_studiengaenge[klausurdaten_plus_studiengaenge["Studiengang"].isnull()].index
    klausurdaten_plus_studiengaenge.loc[leere_studiengaenge, "Studiengang"] = klausurdaten_plus_studiengaenge["Modulnummer"].map(lambda x: "Bachelor" if x < 32000 else "Master")
    return klausurdaten_plus_studiengaenge

    
def replace_semester(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """Ersetzt Wintersemester durch WS und Sommersemester durch SS
    
    Args:
    klausurdaten: Daten über Klausuren
    
    Returns:
    klausurdaten mit abgekürzten Semesternamen
    
    Raises:
    
    Examples:
    
    Note:
    
    """
    klausurdaten_replaced = klausurdaten.copy()
    klausurdaten_replaced["Semester"] = klausurdaten_replaced["Semester"].str.replace("Sommersemester", "SS").str.replace("Wintersemester", "WS")
    
    return klausurdaten_replaced
    
def time_proxy(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """Erstellt eine Datetime-Spalte für Wintersemester und Sommersemester
    
    Args:
    klausurdaten: Daten über Klausuren
    
    Returns
    Daten über Klausuren mit Zeitattribut
    
    Raises:
    
    Examples:
    
    Note:
    Das Zeitattribut ist nötig, um zB in PowerBi sinnvolle Grafiken darzustellen
    """
    klausurdaten_time = klausurdaten.copy()
    
    klausurdaten_time["Zeitpunkt"] = list(map(lambda x: pd.to_datetime(f"01.09.{x[3:]}", format="%d.%m.%Y") if x[:2] \
    == "SS" else pd.to_datetime(f"01.03.{int(x[3:])+1}", format="%d.%m.%Y"), klausurdaten_time["Semester"]))
    
    return klausurdaten_time
    
def summarize_vor_nachklausur(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """Fasst die Ergebnisse von Vor- und Nachklausur zusammen.
    
    Args:
    klausurdaten: Daten über Klausuren
    
    Returns:
    klausurdaten mit unique Werten für Modul und Semester
    
    Raises:
    
    Examples:
    
    Note:
    Seit SS 2024 gibt es zwei Klausurtermine für einige Module. Um die Datenstrukturen konsistent zu halten 
    werden die neuen Vor- und Nachklausuren als eine Klausur angesehen. Das kann die echten Ergebnisse natürlich verzerren.
    """
    klausurdaten_copy = klausurdaten.copy()
    
    klausurdaten_summarized = klausurdaten_copy.groupby(["Modulname", "Modulnummer", "Semester"]) \
    .agg({"Teilnehmer": "sum", "sehr gut": "sum", "gut": "sum", "befriedigend": "sum", "ausreichend": "sum", "nicht ausreichend": "sum", "Zeitpunkt": "max"}) \
    .reset_index()
    
    return klausurdaten_summarized
    
   
def expand_wintersemester(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """Transformiert WS xx zu WS xx/xx+1
    
    Args:
    klausurdaten: Daten über Klausuren
    
    Returns:
    klausurdaten mit jahresübergreifenden Wintersemster-Strings
    
    Raises:
    
    Examples:
    
    Note:
    Diese Funktion ist nötig, da Wintersemester jahresübergreifend sind und ohne diese Funktion eine Sortierung nach Semester
    nicht korrekt funktioniert.
    """
    klausurdaten_replaced = klausurdaten.copy()
    klausurdaten_replaced.loc[klausurdaten_replaced["Semester"].str.startswith("WS"), "Semester"] \
    = list(map(lambda x: f"{x}/{int(x[5:])+1}", klausurdaten_replaced[klausurdaten_replaced["Semester"].str.startswith("WS")]["Semester"]))
    
    return klausurdaten_replaced
    
def concatenate_module(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """Konkateniert Modulnummer und Modulname
    
    Args:
    klausurdaten: Daten über Klausuren
    
    Returns:
    klausurdaten mit konkatenierten Modulnummern- und Modulnamen
    
    Raises:
    
    Examples:
    
    Note:
    Hilfreich für Vilsualisierungen bzw. deren Filterungen
    """
    klausurdaten_concate = klausurdaten.copy()
    klausurdaten_concate["Modul"] = klausurdaten_concate["Modulnummer"].astype("str").str.cat(klausurdaten_concate["Modulname"], sep=" - ")
    
    return klausurdaten_concate

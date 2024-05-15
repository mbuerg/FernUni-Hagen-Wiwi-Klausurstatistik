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
    klausurdaten_durchschnitt["Durchschnittsnote"] = klausurdaten_durchschnitt.iloc[:, 3:9].apply(lambda x: np.sum(x.iloc[1:6] * np.arange(1,6))/x.iloc[0], axis=1)
    klausurdaten_durchschnitt["Durchschnittsnote"] = np.round(klausurdaten_durchschnitt["Durchschnittsnote"], 4)

    return klausurdaten_durchschnitt




def fill_missing_semester(klausurdaten: pd.DataFrame, letztes_jahr: int) -> pd.DataFrame:
    """
        Imputiert ein fehlendes Semester (s). Dabei werden die Teilnehnmer- und Notendaten
        des Semesters s-1 und s+1 gemittelt und als Daten für s verwendet.

    Args:
        klausurdaten (pd.DataFrame): Ein DataFrame mit Modulname- Nummer, Semester,
        Teilnehmer und Noten (1 bis 5) als Spalten. Noten in den Spalten 3 bis 8.
        letztes_jahr (int): Das maximale Jahr, das möglich ist. Beispiel: Das höchste 
        mögliche Semester ist Sommersemester 2024, dann wähle letztes_jahr = 2024.

    Returns:
        pd.DataFrame: klausurdaten mit fehlenden Semestern.
    """
    # Identifiziere welche Semester in den Daten vorhanden sind und welche eigentlich
    # drin sein sollten. Bestimme dann die Differenz
    semester_vorhanden = klausurdaten["Semester"].unique()
    semester_ideal = []
    for i in np.arange(2011, letztes_jahr+1):
        for j in ["Sommersemester ", "Wintersemester "]:
            semester_ideal.append(f"{j}{i}")
    
    semester_fehlend = np.setdiff1d(semester_ideal, semester_vorhanden, assume_unique=True)
    
    # Für jedes fehlende Semester füge es ein und berechne den Durchschnitt des Semesters davor und danach
    klausurdaten_filled = klausurdaten.copy()
    for i, j in enumerate(semester_fehlend):
        
        # Finde die Semester vor und nach dem fehlenden Semester
        semester_fehlend_index = semester_ideal.index(semester_fehlend[i])
        semester_fehlend_vorher = semester_ideal[semester_fehlend_index-1]
        semester_fehlend_nachher = semester_ideal[semester_fehlend_index+1]

        # Finde die Module der Semester davor und danach
        module_fehlend_vorher = klausurdaten_filled.query("Semester == @semester_fehlend_vorher")["Modulnummer"].unique()
        module_fehlend_nachher = klausurdaten_filled.query("Semester == @semester_fehlend_nachher")["Modulnummer"].unique()

        # Welche Module sind in dem Semester davor und danach verfügbar?
        # Die müssen nicht unbedingt gleich sein.
        module_fehlendes_semester = list(np.intersect1d(module_fehlend_vorher, module_fehlend_nachher, assume_unique=True))
        
        # Filterung der relevanten Daten
        klausurdaten_gefiltert_vorher = (klausurdaten_filled
        .query("Semester == @semester_fehlend_vorher & Modulnummer == @module_fehlendes_semester"))
        klausurdaten_gefiltert_nachher = (klausurdaten_filled
        .query("Semester == @semester_fehlend_nachher & Modulnummer == @module_fehlendes_semester"))

        # Berechnung des Durchschnitts durch concat von den Daten davor und danach
        # dann gruppieren, sodass Teilnehmer und jede Note gemittelt ist
        # reset_index() zum Transformieren in einen DataFrame
        klausurdaten_fehlendes_semester = (pd.concat([klausurdaten_gefiltert_vorher
                                            , klausurdaten_gefiltert_nachher])
                                    .groupby(["Modulname"
                                                , "Modulnummer"])[["Teilnehmer"
                                                            , "sehr gut"
                                                            , "gut"
                                                            , "befriedigend"
                                                            , "ausreichend"
                                                            , "nicht ausreichend"]]
                                    .mean()
                                    .reset_index())

        klausurdaten_fehlendes_semester.insert(2, "Semester", j)

        klausurdaten_filled = pd.concat([klausurdaten_filled, klausurdaten_fehlendes_semester]
                                , ignore_index=True)
    
    return klausurdaten_filled




def sort_by_semester(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    """
        Sortiert die klausurdaten und kürzt die Semesterschreibweise ab, sodass 
        nach Modulnummer, Jahr und Semester sortiert ist.

    Args:
        klausurdaten (pd.DataFrame): Ein DataFrame mit Modulname- Nummer, Semester,
        Teilnehmer und Noten (1 bis 5) als Spalten. Semesterdaten in ausgeschriebener
        Weise gegeben, zB Sommersemester 2011 anstatt SS2011

    Returns:
        pd.DataFrame: Sortierte Klausurdaten.
    """
    
    klausurdaten_sortiert = klausurdaten.copy()
    
    # Jahr extrahieren und Abkürzungen erstellen
    klausurdaten_sortiert["Jahr"] = klausurdaten_sortiert["Semester"].apply(lambda x: x[-4:])
    klausurdaten_sortiert["Semester"] = klausurdaten_sortiert["Semester"].str.replace(
        r"Wintersemester \d{4}", "WS", regex = True)
    klausurdaten_sortiert["Semester"] = klausurdaten_sortiert["Semester"].str.replace(
        r"Sommersemester \d{4}", "SS", regex = True)

    # dataframe sortieren
    klausurdaten_sortiert.sort_values(["Modulnummer", "Jahr", "Semester"], inplace = True)

    # Semesterdaten wieder zusammenfügen
    klausurdaten_sortiert["Semester"] = klausurdaten_sortiert["Semester"] + klausurdaten_sortiert["Jahr"]
    del klausurdaten_sortiert["Jahr"]
    
    return klausurdaten_sortiert
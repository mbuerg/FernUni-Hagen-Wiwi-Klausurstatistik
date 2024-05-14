import numpy as np
import pandas as pd

def berechne_durchschnittsnote(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    
    klausurdaten_durchschnitt = klausurdaten.copy()
    klausurdaten_durchschnitt["Durchschnittsnote"] = klausurdaten_durchschnitt.iloc[:, 3:9].apply(lambda x: np.sum(x.iloc[1:6] * np.arange(1,6))/x.iloc[0], axis=1)
    klausurdaten_durchschnitt["Durchschnittsnote"] = np.round(klausurdaten_durchschnitt["Durchschnittsnote"], 4)

    return klausurdaten_durchschnitt





def sort_by_semester(klausurdaten: pd.DataFrame) -> pd.DataFrame:
    
    klausurdaten_sortiert = klausurdaten.copy()
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




def fill_missing_semester(klausurdaten: pd.DataFrame, letztes_jahr: int) -> pd.DataFrame:
    semester_vorhanden = klausurdaten["Semester"].unique()
    semester_ideal = []
    for i in np.arange(2011, letztes_jahr+1):
        for j in ["Sommersemester ", "Wintersemester "]:
            semester_ideal.append(f"{j}{i}")
    
    semester_fehlend = np.setdiff1d(semester_ideal, semester_vorhanden, assume_unique=True)
    
    klausurdaten_filled = klausurdaten.copy()
    for i, j in enumerate(semester_fehlend):
        
        semester_fehlend_index = semester_ideal.index(semester_fehlend[i])
        
        semester_fehlend_vorher = semester_ideal[semester_fehlend_index-1]
        semester_fehlend_nachher = semester_ideal[semester_fehlend_index+1]
    
        module_fehlend_vorher = klausurdaten_filled.query("Semester == @semester_fehlend_vorher")["Modulnummer"].unique()
        module_fehlend_nachher = klausurdaten_filled.query("Semester == @semester_fehlend_nachher")["Modulnummer"].unique()
    
        module_fehlendes_semester = list(np.intersect1d(module_fehlend_vorher, module_fehlend_nachher, assume_unique=True))
        
        klausurdaten_gefiltert_vorher = (klausurdaten_filled
        .query("Semester == @semester_fehlend_vorher & Modulnummer == @module_fehlendes_semester"))

        klausurdaten_gefiltert_nachher = (klausurdaten_filled
        .query("Semester == @semester_fehlend_nachher & Modulnummer == @module_fehlendes_semester"))

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
import numpy as np
import pandas as pd

def berechne_durchschnittsnote(klausurdaten: "pd.DataFrame"):
    
    klausurdaten["Durchschnittsnote"] = klausurdaten.iloc[:, 3:9].apply(lambda x: np.sum(x.iloc[1:6] * np.arange(1,6))/x.iloc[0], axis=1)
    klausurdaten["Durchschnittsnote"] = np.round(klausurdaten["Durchschnittsnote"], 4)

def sort_by_semester(klausurdaten: "pd.DataFrame"):
    
    klausurdaten["Jahr"] = klausurdaten["Semester"].apply(lambda x: x[-4:])
    klausurdaten["Semester"] = klausurdaten["Semester"].str.replace(
        r"Wintersemester \d{4}", "WS", regex = True)
    klausurdaten["Semester"] = klausurdaten["Semester"].str.replace(
        r"Sommersemester \d{4}", "SS", regex = True)

    # dataframe sortieren
    klausurdaten.sort_values(["Modulnummer", "Jahr", "Semester"], inplace = True)

    # Semesterdaten wieder zusammenfügen
    klausurdaten["Semester"] = klausurdaten["Semester"] + klausurdaten["Jahr"]
    #klausurdaten["Jahreszähler"] = str(klausurdaten["Jahr"]) + klausurdaten["Semester"].str[:2]
    #klausurdaten["Jahreszähler"] = klausurdaten["Jahreszähler"].str.replace("WS", "01")
    #klausurdaten["Jahreszähler"] = klausurdaten["Jahreszähler"].str.replace("SS", "02")
    #klausurdaten["Jahreszähler"] = klausurdaten["Jahreszähler"].astype("int32")
    del klausurdaten ["Jahr"]
    




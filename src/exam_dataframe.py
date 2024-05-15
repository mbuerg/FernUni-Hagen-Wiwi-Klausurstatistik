import re

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def build_dataframe(soup: BeautifulSoup, buttons: list) -> pd.DataFrame:
    """
        Transformiert Geparsten HTML Code in einen pandas DataFrame.

    Args:
        soup (BeautifulSoup): Geparster HTML Code
        buttons (list): Liste der Buttons

    Returns:
        pd.DataFrame: DataFrame mit Spalten Modulname- Nummer, Semester,
        Teilnehmer, und den Noten 1 bis 5.
    """
    
    klausurdaten = pd.DataFrame()
    
    for button in np.arange(len(buttons)):
        daten = soup.find("section", {"aria-labelledby":f"button_10_4_0_{button}"})
        daten_str = str(daten)

        
        # Semester
        semester_soup = str(soup.find(id = f"button_10_4_0_{button}"))
        semester = re.search("[WS][a-z]+\s\d+|[WS][a-z]+\s\d+[/]\d+", semester_soup)[0]
        
        # Modulname + sonstiges, sonstiges = Teilnehmer, sehr gut etc
        modul_name_sonstiges = re.findall(r">[^0-9>]{2,}<", daten_str)
        modul_name_sonstiges.append('>Aus Datenschutzgründen entfallen bei weniger als'
                             + ' vier Teilnehmern die Angaben.<')
        modul_name_sonstiges_unique = pd.Series(modul_name_sonstiges).unique()
        modul_name_sonstiges_unique = pd.Series([i.replace("\xad", "") for i in modul_name_sonstiges_unique])
        modul_name_sonstiges_unique = modul_name_sonstiges_unique.str.removeprefix(">")
        modul_name_sonstiges_unique = modul_name_sonstiges_unique.str.removesuffix("<")

        
        modulname = np.setdiff1d(modul_name_sonstiges_unique.unique(), 
                                                       ["sehr gut", "gut", "befriedigend", "ausreichend", "nicht ausreichend", "Teilnehmer"
                                                        , "Aus Datenschutzgründen entfallen bei weniger als vier Teilnehmern die Angaben."]
                                                       , assume_unique=True)
        

        # Modulnummer
        modul_nr = re.findall(r"\d{5}", daten_str)
        
        
        # Teilnehmer und Notenzahlen extrahieren
        teilnehmer_noten = re.findall(r"(>[0-9].[0-9]{1,3}<)|(>—<)|(>–<)|(>-<)|(<td>\s</td>)"
                            +r"|(Aus Datenschutz)|(>[0-9]{1,2}<)", daten_str)

        
        teilnehmer_noten_entpackt = []
        for i in np.arange(len(teilnehmer_noten)):
            if teilnehmer_noten[i][0] != '':
                teilnehmer_noten_entpackt.append(teilnehmer_noten[i][0])
            elif (teilnehmer_noten[i][1] != '') | (teilnehmer_noten[i][2] != '') | (teilnehmer_noten[i][3] != '') | (teilnehmer_noten[i][4] != ''):
                teilnehmer_noten_entpackt.append("0")
            elif (teilnehmer_noten[i][5] != ''):
                teilnehmer_noten_entpackt.extend(["0"]*5)
            else:
                teilnehmer_noten_entpackt.append(teilnehmer_noten[i][6])
            
        teilnehmer_noten_entpackt = (pd.Series(teilnehmer_noten_entpackt).str.replace(".", "")
                                     .str.removeprefix(">")
                                     .str.removesuffix("<")
                                     .astype("int16"))

        # konkrete Zahlen extrahieren
        teilnehmer = pd.Series(extrahiere_teilnehmer(teilnehmer_noten_entpackt))
        sehrgut = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "sehr gut"))
        gut = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "gut"))
        befriedigend = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "befriedigend"))
        ausreichend = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "ausreichend"))
        nicht_ausreichend = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "nicht ausreichend"))
        
        
        # df basteln und im letzten schritt klausurdaten-df updaten
        klausurdaten_ites_semester = pd.concat([pd.Series(modulname)
                                            , pd.Series(modul_nr)
                                        , pd.Series([semester]*len(modul_nr))
                                        , teilnehmer
                                        , sehrgut
                                        , gut
                                        , befriedigend
                                        , ausreichend
                                        , nicht_ausreichend]
                                        , axis=1)
        
        klausurdaten_ites_semester.columns = ["Modulname"
                                              , "Modulnummer"
                                              , "Semester"
                                              , "Teilnehmer"
                                              , "sehr gut"
                                              , "gut"
                                              , "befriedigend"
                                              , "ausreichend"
                                              , "nicht ausreichend"]
        
        
        klausurdaten = pd.concat([klausurdaten, klausurdaten_ites_semester], 
                                axis = 0, ignore_index = True)
    
    
    return klausurdaten



def extrahiere_note(zahlen: pd.Series, note: str) -> list:
    """
        Filtert die Notenzahlen heraus.

    Args:
        zahlen (pd.Series): Modulnummer, Teilnehmer- und Notendaten.
        note (str): sehr gut, gut etc

    Returns:
        list: Liste der Notenzahlen.
    """
    # extrahiert die Anteile an Noten
    match note:
        case "sehr gut":
            note = 2
        case "gut":
            note = 3
        case "befriedigend":
            note = 4
        case "ausreichend":
            note = 5
        case _:
            note = 6
    return [zahlen[i] for i in np.arange(note, len(zahlen), 7)]




def extrahiere_teilnehmer(zahlen: pd.Series) -> list:
    """
        Filtert aus den Teilnehmer- und Notendaten die Teilnehmer
        heraus. Dabei ist zu beachten, dass die Daten die
        Struktur haben Modulnummer, Teilnehmer, dann 5 Notenarten.

    Args:
        zahlen (pd.Series): Modulnummer, Teilnehmer- und Notendaten.

    Returns:
        list: Liste der Teilnehmerzahlen.
    """
    
    # Die letzten Teilnehmer sind das Ende der zahlen - 6.
    # Modulnummern sind > 30000
    teilnehmer = []
    i = 0
    while i <= (len(zahlen) - 6):
        if zahlen.iloc[i+1] < 30000:
            teilnehmer.append(zahlen.iloc[i+1])
            i += 7
        else:
            teilnehmer.append(0)
            i += 1
    return teilnehmer
    
import re

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def extract_examdata(soup: bs4.BeautifulSoup, buttons: list) -> pd.DataFrame:
    """Transformiert Geparsten HTML Code in einen pandas DataFrame.

    Args:
        soup (BeautifulSoup): Geparster HTML Code
        buttons (list): Liste der Buttons

    Returns:
        pd.DataFrame: DataFrame mit Spalten Modulname- Nummer, Semester,
        Teilnehmer, und den Noten 1 bis 5.
    """
    
    klausurdaten = {
        "Modulname": [],
        "Modulnummer": [],
        "Semester": [],
        "Teilnehmer": [],
        "sehr gut": [],
        "gut": [],
        "befriedigend": [],
        "ausreichend": [],
        "nicht ausreichend": [],
    }
    
    for button in buttons:
        sektion = str(soup.find("section", {"aria-labelledby": button}))

        semester = extract_semester(soup, button)
        modulnames = extract_modulenames(sektion)
        modul_nr = parse_modulenumbers_html(sektion)
         
        teilnehmer_noten = extract_participants_grades(sektion)
        teilnehmer_noten_entpackt = unwrap_participants_grades(teilnehmer_noten)

        teilnehmer_anzahl = pd.Series(extrahiere_teilnehmer(teilnehmer_noten_entpackt))
        sehrgut_anzahl = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "sehr gut"))
        gut_anzahl = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "gut"))
        befriedigend_anzahl = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "befriedigend"))
        ausreichend_anzahl = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "ausreichend"))
        nicht_ausreichend_anzahl = pd.Series(extrahiere_note(teilnehmer_noten_entpackt, "nicht ausreichend"))
        
        
        klausurdaten["Modulname"].append(modulnames)
        klausurdaten["Modulnummer"].append(modul_nr)
        klausurdaten["Semester"].append([semester]*len(modul_nr))
        klausurdaten["Teilnehmer"].append(teilnehmer_anzahl)
        klausurdaten["sehr gut"].append(sehrgut_anzahl)
        klausurdaten["gut"].append(gut_anzahl)
        klausurdaten["befriedigend"].append(befriedigend_anzahl)
        klausurdaten["ausreichend"].append(ausreichend_anzahl)
        klausurdaten["nicht ausreichend"].append(nicht_ausreichend_anzahl)
        
    
    klausurdaten_flattened = {k: np.concatenate(v) for k, v in klausurdaten.items()}
    klausurdaten_df = pd.DataFrame(klausurdaten_flattened)
    klausurdaten_df["Modulnummer"] = klausurdaten_df["Modulnummer"].astype("int32")
    
    return klausurdaten_df



def extrahiere_note(zahlen: pd.Series, note: str) -> list:
    """Filtert aus den Teilnehmer- und Notendaten die Noten heraus.
    
    Geht davon aus, dass zB 'sehr gut' an Index 2 für das erste Modul sitzt und alle 7 Indizes weiter 
    für das darauffolgende Modul.

    Args:
    zahlen: Modulnummer, Teilnehmer- und Notendaten.
    note: sehr gut, gut etc

    Returns:
    list: Liste der Notenzahlen.
    
    Raises:
    
    Examples:
    >>> zahlen = pd.Series([
        31001,0,0,0,0,0,0,31011,50,5,15,20,5,5
        ])
    >>> extrahiere_note(zahlen, "sehr gut")
    [np.int64(0), np.int64(5)]
    
    Note:
    
    """
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
    """Filtert aus den Teilnehmer- und Notendaten die Teilnehmer heraus.

    Args:
    zahlen: Modulnummer, Teilnehmer- und Notendaten.

    Returns:
    list: Liste der Teilnehmerzahlen.
    
    Raises:
    
    Examples:
    >>> zahlen = pd.Series([
        31001,0,0,0,0,0,0,31011,50,5,15,20,5,5
        ])
    >>> extrahiere_teilnehmer(zahlen)
    [np.int64(0), np.int64(50)]
        
    Note:
    Die letzten Teilnehmer sind das Ende der zahlen - 6. Modulnummern sind > 30000
    """
    
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
    
def parse_modulenumbers_html(sektion: str) -> list:
    """Findet 5-stelligen Modulnummern in einem String 
    """
    return re.findall("\\d{5}" , sektion)
    
    
    
def extract_modulenames(sektion: str):
    modul_name_sonstiges = re.findall(r">[^0-9>]{2,}<", sektion)
    modul_name_sonstiges.append('>Aus Datenschutzgründen entfallen bei weniger als'
                        + ' vier Teilnehmern die Angaben.<')
    modul_name_sonstiges_unique = pd.Series(pd.Series(modul_name_sonstiges).unique())
    modul_name_sonstiges_unique = modul_name_sonstiges_unique.str.replace("\xad", "")
    modul_name_sonstiges_unique = modul_name_sonstiges_unique.str.removeprefix(">")
    modul_name_sonstiges_unique = modul_name_sonstiges_unique.str.removesuffix("<")
    
    
    modulnamen = np.setdiff1d(modul_name_sonstiges_unique, 
                                ["sehr gut", "gut", "befriedigend", "ausreichend", "nicht ausreichend", "Teilnehmer"
                                 , "Aus Datenschutzgründen entfallen bei weniger als vier Teilnehmern die Angaben."]
                                , assume_unique=True)
    
    return modulnamen
    
def extract_semester(soup: bs4.BeautifulSoup, button: str) -> str:
    semester_soup = str(soup.find(id = button))
    semester = re.search("[WS][a-z]+\\s\\d+|[WS][a-z]+\\s\\d+[/]\\d+", semester_soup)[0]
    
    return semester
    
    
def extract_participants_grades(sektion: str) -> list:
    teilnehmer_noten = re.findall(r"(>[0-9].[0-9]{1,3}<)|(>—<)|(>–<)|(>-<)|(<td>\s</td>)"
                            +r"|(Aus Datenschutz)|(>[0-9]{1,2}<)", sektion)
                            
    return teilnehmer_noten
    

def unwrap_participants_grades(teilnehmer_noten: list) -> pd.Series:
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
                                     .astype("int32"))
                                     
    return teilnehmer_noten_entpackt
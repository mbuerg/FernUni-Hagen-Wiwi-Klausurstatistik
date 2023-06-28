# Skript zum Ziehen der Klausurdaten

import requests
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


#url
URL = "https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/" \
      "klausurstatistik.shtml"
#code scrapen
page = requests.get(URL)
# in soup verwandeln
soup = BeautifulSoup(page.content, "html.parser")
#print(soup)

# alle tables überhaupt
results = soup.find_all("table", class_ = "tabelle100")
#print(results)

# finde alle buttons, über die man iterieren kann!
buttons = re.findall(r'id="button_10_4_0_\d+', str(soup))
#print(len(buttons))

klausurdaten = pd.DataFrame() # muss durch die for loop gefüllt werden
#print(klausurdaten)

for button in np.arange(len(buttons)):
    daten = soup.find("section", {"aria-labelledby":f"button_10_4_0_{button}"})
    daten_str = str(daten)
    #print(daten_str)
    
    # Semester
    semester_soup = str(soup.find(id = f"button_10_4_0_{button}"))
    semester = re.search("[WS][a-z]+\s\d+|[WS][a-z]+\s\d+[/]\d+", semester_soup)[0]
    #print(semester)
    
    # Modulname + sonstiges, sonstiges = Teilnehmer, sehr gut etc
    modul_name_sonstiges = re.findall(r">[^0-9>]{2,}<", daten_str)
    #print(modul_name_sonstiges)
    
    # Sonstiges rauslöschen
    einsen = [1] * len(modul_name_sonstiges)
    vorkommen = pd.DataFrame({"Modulname" : modul_name_sonstiges, 
                                        "Einsen" : einsen})
    #print(vorkommen)


    vorkommen_grouped = vorkommen.groupby("Modulname").count()
    unnoetige_strings = list(vorkommen_grouped[(vorkommen_grouped > 1)["Einsen"]].index)
    unnoetige_strings.append('>Aus Datenschutzgründen entfallen bei weniger als'
                             + ' vier Teilnehmern die Angaben.<')

    #print(unnoetige_strings)
    #print(daten_str)
    
    
    # Lösche unnötige Zeilen
    vorkommen = vorkommen[~vorkommen["Modulname"].isin(unnoetige_strings)]
    vorkommen["Modulname"] = vorkommen["Modulname"].str.removeprefix(">")
    vorkommen["Modulname"] = vorkommen["Modulname"].str.removesuffix("<")
    #print(vorkommen)
    
    # Modulnummer
    modul_nr = re.findall(r"\d{5}", daten_str)
    #print(modul_nr)
    
    
    
    # Teilnehmer und Notenzahlen extrahieren
    zahlen = re.findall(r"(>[0-9].[0-9]{1,3}<)|(>—<)|(>–<)|(>-<)|(<td>\s</td>)"
                        +r"|(Aus Datenschutz)|(>[0-9]{1,2}<)", daten_str)

    
    zahlen_entpackt = []
    for i in np.arange(len(zahlen)):
       if zahlen[i][0] != '':
           zahlen_entpackt.append(zahlen[i][0])
       elif (zahlen[i][1] != '') | (zahlen[i][2] != '') | (zahlen[i][3] != '') | (zahlen[i][4] != ''):
           zahlen_entpackt.append("0")
       elif (zahlen[i][5] != ''):
           zahlen_entpackt.extend(["0"]*5)
       else:
           zahlen_entpackt.append(zahlen[i][6])
          
    
    for i in np.arange(len(zahlen_entpackt)):
            zahlen_entpackt[i] = zahlen_entpackt[i].replace(".", "")

    
    for i in np.arange(len(zahlen_entpackt)):
        zahlen_entpackt[i] = zahlen_entpackt[i].removeprefix(">")
        zahlen_entpackt[i] = zahlen_entpackt[i].removesuffix("<")
    zahlen_entpackt = pd.Series(zahlen_entpackt).astype("int32")

    
    
    # Extrahiere Teilnehmer und Notenzahlen
    def extrahiere_teilnehmer(zahlen):
        # extrahiert die Teilnehmerzahlen
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
    
    
    def extrahiere_note(zahlen, note):
        # extrahiert die Anteile an sehr guten Noten
        if note == "sehr gut":
            note = 2
        elif note == "gut":
            note = 3
        elif note == "befriedigend":
            note = 4
        elif note == "ausreichend":
            note = 5
        else:
            note = 6
        return [zahlen_entpackt[i] for i in np.arange(note, len(zahlen_entpackt), 7)]
    
    

    teilnehmer = pd.Series(extrahiere_teilnehmer(zahlen_entpackt))
    sehrgut = pd.Series(extrahiere_note(zahlen_entpackt, "sehr gut"))
    gut = pd.Series(extrahiere_note(zahlen_entpackt, "gut"))
    befriedigend = pd.Series(extrahiere_note(zahlen_entpackt, "befriedigend"))
    ausreichend = pd.Series(extrahiere_note(zahlen_entpackt, "ausreichend"))
    nicht_ausreichend = pd.Series(extrahiere_note(zahlen_entpackt, "nicht ausreichend"))

    #print(teilnehmer)
    #print(sehrgut)
    #print(gut)
    #print(befriedigend)
    #print(ausreichend)
    #print(nicht_ausreichend)
    
    
    # df basteln und im letzten schritt klausurdaten updaten
    klausurdaten_ites_semester = pd.concat([vorkommen["Modulname"].reset_index(), 
                              pd.Series(modul_nr),
                              pd.Series([semester]*len(modul_nr)), teilnehmer, 
                              sehrgut, gut, befriedigend,
                              ausreichend, nicht_ausreichend], axis = 1)
    
    del klausurdaten_ites_semester["index"]
    
    klausurdaten_ites_semester.columns = ["Modulname", "Modulnummer", "Semester",
                                          "Teilnehmer", "sehr gut", "gut", 
                                          "befriedigend", "ausreichend", 
                                          "nicht ausreichend"]
    
    #print(klausurdaten_ites_semester)
    
    klausurdaten = pd.concat([klausurdaten, klausurdaten_ites_semester], 
                             axis = 0, ignore_index = True)
    
    #print(klausurdaten)
    
#print(klausurdaten)

# Trenne Semester von Jahr
klausurdaten["Jahr"] = klausurdaten["Semester"].apply(lambda x: x[-4:])
klausurdaten["Semester"] = klausurdaten["Semester"].str.replace(
    r"Wintersemester \d{4}", "WS", regex = True)
klausurdaten["Semester"] = klausurdaten["Semester"].str.replace(
    r"Sommersemester \d{4}", "SS", regex = True)

# dataframe sortieren

klausurdaten.sort_values(["Modulnummer", "Jahr", "Semester"], inplace = True)

# Semesterdaten wieder zusammenfügen
klausurdaten["Semester"] = klausurdaten["Semester"] + klausurdaten["Jahr"]
del klausurdaten ["Jahr"]

#print(klausurdaten)
#klausurdaten.to_csv("klausurdaten.csv")

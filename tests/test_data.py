"""
    Dieses Testmodul soll testen welche Eigenschaften die Klausurdaten haben,
    nachdem main.py ausgeführt wurde.
    Sollte es zu Probleme kommen, dass pytest den ABS_PATH in der .env nicht
    erkennt, so kann man 
    
    ABS_PATH="Pfad\\klausurdaten.csv" pytest tests/test_data.py::test_data_duplicates
    
    in Bash zum Beispiel verwenden.
"""

import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def test_data_duplicates():
    testdaten = pd.read_csv(os.getenv("ABS_PATH_FINAL_DATA"))
    duplikate = testdaten.duplicated().sum()
    assert ~(duplikate > 0), f"Es gibt {duplikate} Duplikate"


def test_data_types():
    testdaten = pd.read_csv(os.getenv("ABS_PATH_FINAL_DATA"))
    assert testdaten["Modulname"].dtype == "object", "Modulname ist kein object"
    assert testdaten["Modulnummer"].dtype ==  "int64", "Modulnummer ist kein int64"
    assert testdaten["Semester"].dtype ==  "object", "Semester ist kein object"
    assert testdaten["Teilnehmer"].dtype ==  "int64", "Teilnehmer ist kein int64"
    assert testdaten["sehr gut"].dtype ==  "int64", "sehr gut ist kein int64"
    assert testdaten["gut"].dtype ==  "int64", "gut ist kein int64"
    assert testdaten["befriedigend"].dtype ==  "int64", "befriedigend ist kein int64"
    assert testdaten["ausreichend"].dtype ==  "int64", "ausreichend ist kein int64"
    assert testdaten["nicht ausreichend"].dtype ==  "int64", "nicht ausreichend ist kein int64"
    assert testdaten["Durchschnittsnote"].dtype ==  "float64", "Durchschnittsnote ist kein float64"


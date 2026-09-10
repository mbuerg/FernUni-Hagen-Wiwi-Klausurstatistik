import pandas as pd
import pytest

from src.exam_modifiers import summarize_vor_nachklausur, replace_semester, berechne_durchschnittsnote, fuege_studiengang_hinzu

def test_summarize_vor_nachklausur_wrong_keys():
    df = pd.DataFrame({"a": [5], "b": [3], "c": [6]})
    
    with pytest.raises(KeyError):
        summarize_vor_nachklausur(df)
        
def test_summarize_vor_nachklausur_wrong_aggs():
    df = pd.DataFrame({"Modulname": ["Modul_A"], "Modulnummer": [31025], "Semester": ["SS 2020"], "Teilnehmer": [100]})
    
    with pytest.raises(KeyError):
        summarize_vor_nachklausur(df)
        
def test_replace_semester_wrong_attribute():
    df = pd.DataFrame({"Semester2": ["SS 2020"]})
    
    with pytest.raises(KeyError):
        replace_semester(df)
        
def test_berechne_durchschnittsnote_div_zero():
    df = pd.DataFrame({
        "Modulname": ["Einf"]
        , "Modulnummer": ["33333"]
        , "Semester": ["SS 2020"]
        , "Teilnehmer": [0]
        , "sehr gut": [5]
        , "gut": [10]
        , "befriedigend": [20]
        , "ausreichend": [15]
        , "nicht ausreichend": [50]
    })
    klausurdaten_div_zero = berechne_durchschnittsnote(df)
    
    assert klausurdaten_div_zero.at[0, "Durchschnittsnote"] == 0
    
def test_berechne_durchschnittsnote_wrong_attribute_order():
    df = pd.DataFrame({
        "Modulname": ["Einf"]
        , "Modulnummer": [33333]
        , "Teilnehmer": [100]
        , "sehr gut": [5]
        , "gut": [10]
        , "befriedigend": [20]
        , "ausreichend": [15]
        , "nicht ausreichend": [50]
        , "Semester": ["SS 2020"]
    })
    
    with pytest.raises(TypeError):
        berechne_durchschnittsnote(df)
        
def test_fuege_studiengang_hinzu_no_modulnumber():
    df = pd.DataFrame({"a": [5], "Modulnummer": [33333]})
    df2 = pd.DataFrame({"a": [5], "b": [33333]})
    
    with pytest.raises(KeyError):
        fuege_studiengang_hinzu(df, df2)
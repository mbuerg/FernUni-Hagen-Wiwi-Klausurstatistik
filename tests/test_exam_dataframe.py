import pytest
import pandas as pd

from src.exam_dataframe import extrahiere_note, extract_examdata

def test_extrahiere_note_wrong_grade():
    note = "hello world"
    zahlen = pd.Series([31001, 20,2,3,4,5,6])
    
    assert extrahiere_note(zahlen, note) == [6]
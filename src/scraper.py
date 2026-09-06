import re

import pandas as pd
import numpy as np
import requests
from PyPDF2 import PdfReader
from pyprojroot import here
from bs4 import BeautifulSoup

def concatenate_bachelor_and_master(bachelor: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:

    alle_module = (pd.concat([bachelor, master])
                .reset_index(drop=True))

    # es gibt Module, die in Bachelor und Masterstudiengang absolviert werden können
    # wenn in beiden, dann Bachelor
    #doppelte_raus = alle_module[alle_module["Modulnummer"].isin(bachelor["Modulnummer"])]
    #doppelte_raus["Studiengang"] = "Bachelor"

    alle_module_bereinigt = alle_module.sort_values(by=["Modulnummer", "Studiengang"]) \
        .drop_duplicates(subset=["Modulnummer"]).reset_index(drop=True)
    
    return alle_module_bereinigt



def extract_modulenumbers(bachelor: bool = True) -> pd.DataFrame:
    ROOT_DIR = here()
    if not bachelor:
        reader = PdfReader(ROOT_DIR / "Modulnummern" / "master.pdf")
        studiengang = "Master"
    else:
        reader = PdfReader(ROOT_DIR / "Modulnummern" / "bachelor.pdf")
        studiengang = "Bachelor"
    number_of_pages = len(reader.pages)
    module = np.array([])

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        module = (np.append(module
                            , parse_modulenumbers(text))
                        .astype("int64"))
    module_df = (pd.DataFrame({"Modulnummer": module})
                 .sort_values("Modulnummer")
                 .reset_index(drop=True))
    module_df["Studiengang"] = studiengang
    
    return module_df


def parse_modulenumbers(text: str) -> pd.Series:

    return pd.Series(re.findall("\n\\d{5}" , text)).str[1:]


def scrape_web() -> BeautifulSoup | list:
    """
        Scraped die Seite der Wiwi Klausurstatistiken der FernUni Hagen.
        Die Daten werden per request geholt, dann per soup geparsed
        und alle buttons, sowie soup ausgegeben. Die Buttons sind 
        im html code gerade die Buttons, die für die einzelnen Semester
        stehen.
    Args:
        None
    
    Returns:
        soup (BeautifulSoup): Geparseder HTML Code
        buttons (list): Liste der Buttons im HTML Code
    """
    #url
    URL = "https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/" \
        "klausurstatistik.shtml"
    
    try:
        # page.content beinhaltet den html code
        page = requests.get(URL)
    except Exception as e:
        raise RuntimeError(f"Netzwerkfehler: {e}")
        
    page.raise_for_status()
    
    try:
        # html code parsen
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        raise RuntimeError(f"Fehler beim Parsen der HTML: {e}")
    
    try:
        # Tables sind die einzelnen Tabelle für ein Modul
        results = soup.find_all("table", class_ = "tabelle100")
        # Buttons sind Buttons für Sommersemester 2023 etc zum Aufklappen.
        buttons = re.findall(r'id="button_10_\d+_\d+_\d+', str(soup))
    except Exception as e:
        raise RuntimeError(f"Fehler beim Extrahieren der Buttons: {e}")
    
    return soup, buttons
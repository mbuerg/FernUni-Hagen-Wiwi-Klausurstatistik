import re

import pandas as pd
import numpy as np
import requests
from PyPDF2 import PdfReader
from pyprojroot import here
from bs4 import BeautifulSoup

def concatenate_bachelor_and_master(bachelor: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:
    """Fügt Bachelor- und Mastermodule zusammen
    
    Args:
    bachelor: Spalte mit Modulnummer und konstante Spalte mit "Bachelor"
    master: Spalte mit Modulnummer und konstante Spalte mit "Master"
    
    Returns:
    Konkatenation von Bachelor- und Mastermodulen
    
    Raises:
    
    Examples:
    concatenate_bachelor_and_master(bachelor_modules, master_modules)
    
    Note:
    Bachelor- und Mastermodulen sind nicht disjunkt. Wenn Modul in beiden Studiengängen, dann wird es als bachelor gesetzt.
    """

    alle_module = (pd.concat([bachelor, master])
                .reset_index(drop=True))

    alle_module_bereinigt = alle_module.sort_values(by=["Modulnummer", "Studiengang"]) \
        .drop_duplicates(subset=["Modulnummer"]).reset_index(drop=True)
    
    return alle_module_bereinigt



def extract_modulenumbers(bachelor: bool = True) -> pd.DataFrame:
    """Findet Modulnummern und weist denen Bachelor/Master zu.
    
    Args:
    bachelor: Gibt an, ob die Datei sich auf Bachelor (default) oder Master (False) bezieht
    
    Returns:
    Modulnummern und Spalte, ob diese Bachelor oder Master sind
    
    Raises:
    
    Examples:
    extract_modulenumbers(bachelor = False)
    
    Note:
    TODO: Eventuell ROOT_DIR ändern und den User einen Pfas eingeben lassen
    """
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
                            , parse_modulenumbers_pdf(text))
                        .astype("int64"))
    module_df = (pd.DataFrame({"Modulnummer": module})
                 .sort_values("Modulnummer")
                 .reset_index(drop=True))
    module_df["Studiengang"] = studiengang
    
    return module_df


def parse_modulenumbers_pdf(text: str) -> pd.Series:
    """Findet 5-stelligen Modulnummern in einem String 
    """
    return pd.Series(re.findall("\n\\d{5}" , text)).str[1:]


def scrape_web() -> bs4.BeautifulSoup:
    """Scraped die Seite der Wiwi Klausurstatistiken der FernUni Hagen und parsed Buttons und Tabellen
    
    Args:
    None
    
    Returns:
    soup: Geparseder HTML Code
    buttons: Liste der Buttons im HTML Code
    
    Raises:
    RuntimeError: Falls beim Request oder parsen etwas schief geht, macht eine Fortsetzung des Programms keinen weiteren Sinn
    HTTPError: Falls client error oder server error
    
    Examples:
    soup = scrape_web()
    
    Note:
    TODO: Parsing auslagern
    """
    
    URL = "https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/" \
        "klausurstatistik.shtml"
    
    try:
        page = requests.get(URL)
    except Exception as e:
        raise RuntimeError(f"Netzwerkfehler: {e}")
        
    page.raise_for_status()
    
    try:
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        raise RuntimeError(f"Fehler beim Parsen der HTML: {e}")
    
    return soup
    

def extract_buttons(soup: bs4.BeautifulSoup) -> list[str]:
    """Extrahiert die HTML-Buttons, die die Semester strukturieren
    
    Args:
    html_page: 
    
    Returns:
    Buttons auf der Seite der Klausurstatistiken
    
    Raises:
    RuntimeError: Falls beim Extrahieren etwas schief geht, macht eine Fortsetzung des Programms keinen weiteren Sinn
    
    Examples:
    
    Note:
    
    """

    try:
        results = soup.find_all("table", class_ = "tabelle100")
        buttons = re.findall(r'id="button_10_\d+_\d+_\d+', str(soup))
    except Exception as e:
        raise RuntimeError(f"Fehler beim Extrahieren der Buttons: {e}")
        
    buttons_stripped = list(map(lambda x: x[4:], buttons))
    
    return buttons_stripped
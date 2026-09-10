import re

import pandas as pd
import numpy as np
import requests
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup


class NoButtonsException(Exception):
    pass


def concatenate_bachelor_and_master(bachelor: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:
    """Fügt Bachelor- und Mastermodulnummern zusammen
    
    Args:
    bachelor: Spalte mit Modulnummer und konstante Spalte mit "Bachelor"
    master: Spalte mit Modulnummer und konstante Spalte mit "Master"
    
    Returns:
    Konkatenation von Bachelor- und Mastermodulen
    
    Raises:
    
    Examples:
    concatenate_bachelor_and_master(bachelor_modules, master_modules)
    
    Note:
    Bachelor- und Mastermodulen sind nicht disjunkt. Wenn Modul in beiden Studiengängen ist, dann wird es als Bachelor gesetzt.
    """

    alle_module = (pd.concat([bachelor, master])
                .reset_index(drop=True))

    alle_module_bereinigt = alle_module.sort_values(by=["Modulnummer", "Studiengang"]) \
        .drop_duplicates(subset=["Modulnummer"]).reset_index(drop=True)
    
    return alle_module_bereinigt



def extract_modulenumbers(path: str, studiengang: str) -> pd.DataFrame:
    """Findet Modulnummern und weist denen Bachelor/Master zu.
    
    Args:
    path: Pfad zu einer pdf mit den Modulnummern des Bachelor oder Master
    studiengang: Bachelor oder Master
    
    Returns:
    Modulnummern und Spalte, ob diese Bachelor oder Master sind
    
    Raises:
    
    Examples:
    extract_modulenumbers(bachelor = False)
    
    Note:
    """
        
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    module = np.array([])

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        module = (np.append(module
                            , parse_modulenumbers_pdf(text)).astype("int32"))
    module_df = (pd.DataFrame({"Modulnummer": module})
                 .sort_values("Modulnummer")
                 .reset_index(drop=True))
    module_df["Studiengang"] = studiengang
    
    return module_df


def parse_modulenumbers_pdf(text: str) -> pd.Series:
    r"""Findet 5-stelligen Modulnummern untereinander aufgelistet in einem String 
    
    Args:
    text: Enthält zeilenweise Auflistung mit 5-stelligen Nummern
    
    Returns:
    5-stellige Nummern
    
    Raises:
    
    Examples:
    >>> text='\n31721\n31751\n31771'
    >>> parse_modulenumbers_pdf(text)
    0    31721
    1    31751
    2    31771
    dtype: str
    
    >>> text='abc456\n1234'
    >>> parse_modulenumbers_pdf(text)
    Series([], dtype: object)
    
    Note:
    
    """
    return pd.Series(re.findall("\n\\d{5}" , text)).str[1:]


def scrape_web(URL: str) -> bs4.BeautifulSoup:
    """Scraped die Seite der Wiwi Klausurstatistiken der FernUni Hagen und parsed Buttons und Tabellen
    
    Args:
    URL: URL der Wiwi Klausurdaten der FernUni Hagen
    
    Returns:
    soup: Geparseder HTML Code
    
    Raises:
    RequestException: Falls beim Request  etwas schief geht, macht eine Fortsetzung des Programms keinen weiteren Sinn
    
    Examples:
    soup = scrape_web('https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/klausurstatistik.shtml')
    
    Note:
    """
    
    page = requests.get(URL)
    page.raise_for_status()
    
    soup = BeautifulSoup(page.content, "html.parser")

    return soup
    

def extract_buttons(soup: bs4.BeautifulSoup) -> list[str]:
    """Extrahiert die HTML-Buttons, die die Semester strukturieren
    
    Args:
    soup: HTML-Code der geparsten Seite
    
    Returns:
    Buttons auf der Seite der Klausurstatistiken
    
    Raises:
    NoButtonsException: Falls der HTML-Code keine Buttons enthält
    
    Examples:
    >>> extract_buttons('id="button_10_0_0_0"')
    ['button_10_0_0_0']
    
    Note:
    
    """

    buttons = re.findall(r'id="button_10_\d+_\d+_\d+', str(soup))
    if not buttons:
        raise NoButtonsException("Es sind keine Buttons zu finden")
        
    buttons_stripped = list(map(lambda x: x[4:], buttons))
    
    return buttons_stripped
    
if __name__ == "__main__":
    pass
import re

import requests
from bs4 import BeautifulSoup

def scrape() -> BeautifulSoup | list:
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
    
    try:
        # in soup verwandeln. Dadurch wird der html code geparsed
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        raise RuntimeError(f"Fehler beim Parsen der HTML: {e}")
    
    try:
        # alle tables überhaupt. Tables sind die einzelnen Tabelle für ein Modul
        results = soup.find_all("table", class_ = "tabelle100")
        # finde alle buttons, über die man iterieren kann!
        # Buttons sind Buttons für Sommersemester 2023 etc zum Aufklappen.
        buttons = re.findall(r'id="button_10_4_0_\d+', str(soup))
    except Exception as e:
        raise RuntimeError(f"Fehler beim Extrahieren der Buttons: {e}")
    
    return soup, buttons
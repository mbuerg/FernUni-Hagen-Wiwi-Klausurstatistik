import re

import requests
from bs4 import BeautifulSoup

def scrape():
    #url
    URL = "https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/" \
        "klausurstatistik.shtml"
    #code scrapen
    # paghe.content beinhaltet den html code
    page = requests.get(URL)
    # in soup verwandeln. Dadurch wird der html code sortiert/geparsed
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup)

    # alle tables überhaupt. Tables sind die einzelnen Tabelle für ein Modul
    results = soup.find_all("table", class_ = "tabelle100")
    #print(results)

    # finde alle buttons, über die man iterieren kann!
    # Buttons sind Buttons für Sommersemester 2024 etc zum Aufklappen.
    buttons = re.findall(r'id="button_10_4_0_\d+', str(soup))
    #print(len(buttons))
    return soup, buttons
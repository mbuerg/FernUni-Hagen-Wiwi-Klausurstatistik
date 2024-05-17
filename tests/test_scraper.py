import requests
from bs4 import BeautifulSoup

import src.scraper


def test_url():
    URL = "https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/" \
        "klausurstatistik.shtml"
    
    response = requests.get(URL)
    
    assert response.status_code == 200, f"URL nicht erreichbar wegen: {response.status_code}"



def test_scrape_types():
    a, b = src.scraper.scrape()
    assert isinstance(a, BeautifulSoup)
    assert isinstance(b, list)



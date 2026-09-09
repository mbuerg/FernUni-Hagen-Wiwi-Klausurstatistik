import pytest
import requests
import pandas as pd
from bs4 import BeautifulSoup

from src.scraper import scrape_web, extract_modulenumbers, concatenate_bachelor_and_master, extract_buttons


def test_scrape_web_wrong_url(mocker) -> None:
    wrong_url = "https://unsinnige-url.de"
    mocker.patch("src.scraper.requests.get", side_effect=requests.exceptions.InvalidURL("Falsche URL"))
    
    with pytest.raises(requests.exceptions.InvalidURL):
        scrape_web(wrong_url)
        
        
def test_scrape_web_connection_error(mocker) -> None:
    mocker.patch("src.scraper.requests.get", side_effect=requests.exceptions.ConnectionError("Verbindung nicht hergestellt"))
    
    with pytest.raises(requests.exceptions.ConnectionError):
        scrape_web("https://www.scrapethissite.com/pages/")


def test_scrape_web_response_404(mocker) -> None:
    mock_response = mocker.MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Fehler")
    mocker.patch("src.scraper.requests.get", return_value=mock_response)
    
    with pytest.raises(requests.exceptions.HTTPError):
        scrape_web("https://www.scrapethissite.com/pages/")


def test_scrape_web_response_type() -> None:
    result = scrape_web("https://www.scrapethissite.com/pages/")
    assert isinstance(result, BeautifulSoup)




def test_extract_modulenumbers_wrong_path() -> None:
    path = "non_existing_path"
    
    with pytest.raises(FileNotFoundError):
        extract_modulenumbers(path, "Bachelor")

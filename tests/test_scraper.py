from bs4 import BeautifulSoup

import src.scraper


def test_scrape_types():
    a, b = src.scraper.scrape()
    assert isinstance(a, BeautifulSoup)
    assert isinstance(b, list)



"""
    Dieses Testmodul testet die Funktionalität des PDF Scrapers
    In Powershell ausführen: pytest tests/test_pdf_scraper.py
"""

import pandas as pd

import src.pdf_scraper


def test_concatenate_bachelor_and_master_types() -> None:
    bachelor = src.pdf_scraper.extract_modulenumbers("BACHELOR")
    master = src.pdf_scraper.extract_modulenumbers("MASTER")
    
    assert isinstance(src.pdf_scraper.concatenate_bachelor_and_master(bachelor, master), pd.DataFrame)



def test_extract_modulenumbers_types() -> None:
    bachelor = src.pdf_scraper.extract_modulenumbers("BACHELOR")
    master = src.pdf_scraper.extract_modulenumbers("MASTER")
    
    assert isinstance(bachelor, pd.DataFrame)
    assert isinstance(master, pd.DataFrame)


def test_parse_modulenumbers_cases():
    assert src.pdf_scraper.parse_modulenumbers("Some text\n12345\nmore text\n67890").equals(pd.Series(['12345', '67890']))
    assert src.pdf_scraper.parse_modulenumbers("hallo welt!!").equals(pd.Series([]))
    assert src.pdf_scraper.parse_modulenumbers("12345").equals(pd.Series([]))
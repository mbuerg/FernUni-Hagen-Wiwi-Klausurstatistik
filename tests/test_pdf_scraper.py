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


import pandas as pd
import logging

from pyprojroot import here

from src.scraper import extract_modulenumbers, concatenate_bachelor_and_master, scrape_web, extract_buttons
from src.exam_dataframe import extract_examdata
from src.exam_modifiers import replace_semester, time_proxy, summarize_vor_nachklausur, expand_wintersemester, berechne_durchschnittsnote, fuege_studiengang_hinzu, concatenate_module
from src.logger import setup_logging


def main(url, path_bachelor, path_master):
    soup = scrape_web(url)
    buttons = extract_buttons(soup)
    bachelor_module = extract_modulenumbers(path_bachelor, "Bachelor")
    master_module = extract_modulenumbers(path_master, "Master")
    module_gesamt = concatenate_bachelor_and_master(bachelor_module, master_module)
    klausurdaten = extract_examdata(soup, buttons)
    klausurdaten_replaced = replace_semester(klausurdaten)
    klausurdaten_replaced_time = time_proxy(klausurdaten_replaced)
    klausurdaten_replaced_time_summarized = summarize_vor_nachklausur(klausurdaten_replaced_time)
    klausurdaten_replaced_time_summarized_expanded = expand_wintersemester(klausurdaten_replaced_time_summarized)
    klausurdaten_replaced_time_summarized_expanded_avg = berechne_durchschnittsnote(klausurdaten_replaced_time_summarized_expanded)
    klausurdaten_replaced_time_summarized_expanded_avg_studiengang = fuege_studiengang_hinzu(klausurdaten_replaced_time_summarized_expanded_avg
                                                                                                , module_gesamt)
    klausurdaten_replaced_time_summarized_expanded_avg_studiengang_conc = concatenate_module(klausurdaten_replaced_time_summarized_expanded_avg_studiengang)
    klausurdaten_replaced_time_summarized_expanded_avg_studiengang_conc.to_csv("data/klausurdaten.csv", index=False)
    
if __name__ == "__main__":
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("----Programmstart----")
    
    URL = "https://www.fernuni-hagen.de/wirtschaftswissenschaft/studium/" \
        "klausurstatistik.shtml"
    PATH_BACHELOR = here() / "Modulnummern" / "bachelor.pdf"
    PATH_MASTER = here() / "Modulnummern" / "master.pdf"
    
    main(URL, PATH_BACHELOR, PATH_MASTER)
    
    logger.info("----Programm erfolgreich beendet----")
import pandas as pd

import scraper
import exam_dataframe
import exam_modifiers
import pdf_scraper


def main():
    soup, buttons = scraper.scrape()
    bachelor_module = pdf_scraper.extract_modulenumbers("BACHELOR")
    master_module = pdf_scraper.extract_modulenumbers("MASTER")
    module_gesamt = pdf_scraper.concatenate_bachelor_and_master(bachelor_module, master_module)
    klausurdaten = exam_dataframe.build_dataframe(soup, buttons)
    klausurdaten_filled = exam_modifiers.fill_missing_semester(klausurdaten=klausurdaten
                                                               , letztes_jahr= 2023)
    klausurdaten_filled_average = exam_modifiers.berechne_durchschnittsnote(klausurdaten_filled)
    klausurdaten_filled_average_sortiert = exam_modifiers.sort_by_semester(klausurdaten_filled_average)
    klausurdaten_filled_average_sortiert_studiengaenge = exam_modifiers.fuege_studiengang_hinzu(klausurdaten_filled_average_sortiert
                                                                                                , module_gesamt)
    klausurdaten_filled_average_sortiert_studiengaenge_semesteralias = exam_modifiers.aliasing_semester(klausurdaten_filled_average_sortiert_studiengaenge, 2023)
    klausurdaten_filled_average_sortiert_studiengaenge_semesteralias.to_csv("../data/klausurdaten.csv", index=False)

if __name__ == "__main__":
    main()
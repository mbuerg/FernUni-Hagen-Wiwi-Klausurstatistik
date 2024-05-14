import pandas as pd

import scraper
import exam_dataframe
import exam_modifiers


def main():
    soup, buttons = scraper.scrape()
    klausurdaten = exam_dataframe.build_dataframe(soup, buttons)
    klausurdaten_gesamt = exam_modifiers.fill_missing_semester(klausurdaten=klausurdaten
                                                               , letztes_jahr= 2023)
    exam_modifiers.berechne_durchschnittsnote(klausurdaten_gesamt)
    exam_modifiers.sort_by_semester(klausurdaten_gesamt)
    klausurdaten_gesamt.to_csv("../data/klausurdaten.csv", index=False)


if __name__ == "__main__":
    main()
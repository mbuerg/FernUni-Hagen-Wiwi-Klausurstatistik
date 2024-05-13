import pandas as pd

import scraper
import exam_dataframe
import exam_modifiers


def main():
    soup, buttons = scraper.scrape()
    klausurdaten = exam_dataframe.build_dataframe(soup, buttons)
    exam_modifiers.berechne_durchschnittsnote(klausurdaten)
    exam_modifiers.sort_by_semester(klausurdaten)
    klausurdaten.to_csv("../data/klausurdaten.csv", index=False)


if __name__ == "__main__":
    main()
import pandas as pd

import scraper
import exam_dataframe
import durchschnittsnote


def main():
    soup, buttons = scraper.scrape()
    klausurdaten = exam_dataframe.build_dataframe(soup, buttons)
    durchschnittsnote.berechne_durchschnittsnote(klausurdaten)
    klausurdaten.to_csv("klausurdaten_test.csv", index=False)


if __name__ == "__main__":
    main()
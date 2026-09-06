import pandas as pd

from scraper import extract_modulenumbers, concatenate_bachelor_and_master, scrape_web
from exam_dataframe import build_dataframe
from exam_modifiers import replace_semester, time_proxy, summarize_vor_nachklausur, expand_wintersemester, berechne_durchschnittsnote, fuege_studiengang_hinzu, concatenate_module


def main():
    soup, buttons = scrape_web()
    bachelor_module = extract_modulenumbers()
    master_module = extract_modulenumbers(bachelor=False)
    module_gesamt = concatenate_bachelor_and_master(bachelor_module, master_module)
    klausurdaten = build_dataframe(soup, buttons)
    klausurdaten_replaced = replace_semester(klausurdaten)
    klausurdaten_replaced_time = time_proxy(klausurdaten_replaced)
    klausurdaten_replaced_time_summarized = summarize_vor_nachklausur(klausurdaten_replaced_time)
    klausurdaten_replaced_time_summarized_expanded = expand_wintersemester(klausurdaten_replaced_time_summarized)
    klausurdaten_replaced_time_summarized_expanded_avg = berechne_durchschnittsnote(klausurdaten_replaced_time_summarized_expanded)
    klausurdaten_replaced_time_summarized_expanded_avg_studiengang = fuege_studiengang_hinzu(klausurdaten_replaced_time_summarized_expanded_avg
                                                                                                , module_gesamt)
    klausurdaten_replaced_time_summarized_expanded_avg_studiengang_conc = concatenate_module(klausurdaten_replaced_time_summarized_expanded_avg_studiengang)
    klausurdaten_replaced_time_summarized_expanded_avg_studiengang_conc.to_csv("../data/klausurdaten.csv", index=False)

if __name__ == "__main__":
    main()
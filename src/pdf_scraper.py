import re
import os

import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()


def concatenate_bachelor_and_master(bachelor: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:

    alle_module = (pd.concat([bachelor, master])
                .reset_index(drop=True))

    # es gibt Module, die in Bachelor und Masterstudiengang absolviert werden können
    # wenn in beiden, dann Bachelor
    doppelte_raus = alle_module[alle_module["Modulnummer"].isin(bachelor["Modulnummer"])]
    doppelte_raus["Studiengang"] = "Bachelor"

    alle_module_bereinigt = alle_module[~alle_module.duplicated("Modulnummer")]
    
    return alle_module_bereinigt



def extract_modulenumbers(BACHELOR_or_MASTER: str) -> pd.DataFrame:
    
    reader = PdfReader(os.getenv("ABS_PATH_"+BACHELOR_or_MASTER))
    number_of_pages = len(reader.pages)
    module = np.array([])

    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        module = (np.append(module
                            , parse_modulenumbers(text))
                        .astype("int64"))
    module_df = (pd.DataFrame({"Modulnummer": module})
                 .sort_values("Modulnummer")
                 .reset_index(drop=True))
    module_df["Studiengang"] = BACHELOR_or_MASTER.capitalize()
    
    return module_df


def parse_modulenumbers(text: str) -> pd.Series:

    return pd.Series(re.findall("\n\d{5}" , text)).str[1:]
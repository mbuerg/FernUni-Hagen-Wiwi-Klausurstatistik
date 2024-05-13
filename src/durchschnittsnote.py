import numpy as np
import pandas as pd

def berechne_durchschnittsnote(klausurdaten: "pd.DataFrame"):
    
    klausurdaten["Durchschnittsnote"] = klausurdaten.iloc[:, 3:9].apply(lambda x: np.sum(x.iloc[1:6] * np.arange(1,6))/x.iloc[0], axis=1)
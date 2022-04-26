


import pandas as pd

import pickle


def dame_reglas():

    with open('results.pkl', 'rb') as f:
        results = pickle.load(f)

    from apyori import inspect

    frame = pd.DataFrame(inspect(results),columns = ["comprados","item","soporte","confianza","list"])

    def limpia(dato):
        dato = dato.replace("(","")
        dato = dato.replace(")","")
        dato = dato.replace(",","")
        dato = dato.replace("'","")
        dato = dato.replace(" ","")
        dato = dato.replace("None","")
        return dato

    frame["comprados"] = frame["comprados"].apply(str)
    frame["item"] = frame["item"].apply(str)
    frame["comprados"] = frame["comprados"].apply(limpia)
    frame["item"] = frame["item"].apply(limpia)


    dict_regla = {}
    for ind in frame.index:
        dict_regla[frame["item"][ind]] = frame["comprados"][ind]


    return dict_regla


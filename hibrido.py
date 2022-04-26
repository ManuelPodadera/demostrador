
import pandas as pd
from operator import itemgetter

from collaborative import resultado_colaborativo
from content import recomendacion_content_based


df = pd.read_csv("user_name_group.csv",header=0)
dict_user_name = {}
for ind in df.index:
    dict_user_name[df["reviewerID"][ind]] = df["grupo"][ind]


def recomendacion_hibrida(user,asin):

    
    rec_cola = resultado_colaborativo(user)

    dicc_colaborativo = {}
    for i in rec_cola:
        dicc_colaborativo[i[0]] = i[1]

    rec_cont = recomendacion_content_based(asin)

    todas_las_recomendaciones = set(dicc_colaborativo.keys()) | set(rec_cont)

    grupo = dict_user_name[user]

    if grupo == "A":
        content_factor = 0.5

    if grupo == "B":
        content_factor = 1.5
    
    L = []
    for item in todas_las_recomendaciones:
        valoracion = 0
        if item in dicc_colaborativo.keys():
            valoracion = valoracion + dicc_colaborativo[item]
        if item in rec_cont:
            valoracion = valoracion * content_factor

        L.append([item,round(valoracion/2,2)])

    L = sorted(L, key=itemgetter(1))
    L.reverse()

    resul = []
    for i in L[:10]:
        resul.append(i[0])

    return resul

#print(recomendacion_hibrida("A1063BS4W8YHHE","B00005N7PN"))
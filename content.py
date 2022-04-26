#Cargamos todas las librerias necesarias

import pandas as pd
import numpy as np
import pickle

# Utilizaremos 
# Convert a collection of text documents to a matrix of token counts.
# https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd
from sklearn.neighbors import NearestNeighbors

from operator import itemgetter

data = pd.read_csv("datos_para_content.csv",header=0)

cv = CountVectorizer()
count_matrix = cv.fit_transform(data["combinado"])

#pickle.dump(model, open("modelo_content.pkl", 'wb'))
model = pickle.load(open("modelo_content.pkl", 'rb'))

def recomendacion_content_based(asin):

    dicc_index_url = {}
    for ind in data.index:
        dicc_index_url[ind]=data["asin"][ind]

    def dame_indice_de_este_valor(data,item):
        return data.index[data['asin'] == item].tolist()[0]

    def recommender(data, n_recommendations, idx, model):
        distances, indices = model.kneighbors(data[idx], n_neighbors=n_recommendations)
        return indices

    idx = dame_indice_de_este_valor(data,asin)

    indices = recommender(count_matrix, 10, idx, model)

    resultado = []
    for i in indices[0]:
        resultado.append(dicc_index_url[i])

    return resultado


#print(recomendacion_content_based("B00005N7PN"))
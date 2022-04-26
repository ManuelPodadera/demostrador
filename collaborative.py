import pandas as pd
from operator import itemgetter
import surprise

df = pd.read_csv('Users.csv')

# reordenamos las columnas
df = df[["reviewerID","asin","overall"]]


from surprise import Dataset, Reader
from surprise import SVD

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[["reviewerID","asin","overall"]], reader)

algo = SVD(n_factors = 30, n_epochs = 70, lr_all = 0.006, reg_all =  0.04)
train = data.build_full_trainset()
algo.fit(train)

#surprise.dump.dump("filtrado_colaborativo.pkl", predictions=None, algo=algo, verbose=0)

def resultado_colaborativo(usuario):
    no_valoradas = list(set(list(df[df["reviewerID"]!=usuario]["asin"])))
    L = []
    for item in no_valoradas:
        
        val = algo.predict(uid = usuario, iid = item)
        L.append([val[1],val[3]])
    L = sorted(L, key=itemgetter(1))
    L.reverse()
    #print(L)
    return L

    
# print(resultado_colaborativo("A1063BS4W8YHHE"))
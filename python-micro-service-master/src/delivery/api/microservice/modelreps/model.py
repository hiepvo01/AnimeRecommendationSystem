import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from sklearn import preprocessing
from delivery.api.microservice.modelreps.db import first_filtered, genres, user_default, use_cols, response_default, df_model
from sklearn.neighbors import KNeighborsClassifier

# KNN with KNeighborsClassifier to predict anime Score
# To use scikit-learn library, we have to convert the Pandas data frame to a Numpy array:
# For this model, I round the score column to integers instead of floats
scores = []
for score in df_model.score:
    scores.append(round(score))
Y = pd.DataFrame(scores)

df_model1 = df_model

use_cols = list(df_model1.columns)
if 'score' in use_cols:
    use_cols.remove('score')
if 'title' in use_cols:
    use_cols.remove('title')
X = df_model1[use_cols].values  #.astype(float)
y = Y[0].values
#Normalize Data
x = preprocessing.StandardScaler().fit(X).transform(X.astype(float))

#Train Test Split
from sklearn.model_selection import train_test_split
neigh = KNeighborsClassifier(n_neighbors = 7).fit(x, y)  

from sklearn.neighbors import NearestNeighbors
# Here I use the Nearest Neighbor model to find the nearest 5 similar animes 
# (closest distances between the animes' attributes)
rec_neigh = NearestNeighbors(n_neighbors=6, algorithm='auto').fit(X)
distances, indexs = rec_neigh.kneighbors(X)

# Return the Index of the anime if its name is given in full
# Warning, the name has to be exact, even the upper case letters.
def full_id(name):
    try:
        df_model1[df_model1["title"] == name].index.tolist()[0]
        return df_model1[df_model1["title"] == name].index.tolist()[0]
    except:
        return "This is not a valid full name"

all_names = list(df_model1.title.values)

# If you only know a part of the anime name, you can get the list of possible full anime names, 
# The input can be lower case
def part_id(part):
    full_list = []
    for name in all_names:
        if part.lower() in name.lower():
            full_list.append(name)
    return full_list
            
# Can get similar animes with input of anime name or anime index

def similar_animes(query=None,id=None):
    similars = []
    if id:
        for id in indexs[id][1:]:
            similars.append(df_model1.iloc[id]["title"])
    if query:
        found_id = full_id(query)
        if found_id == "This is not a valid full name":
            similars.append(found_id)
        else:
            for id in indexs[found_id][1:]:
                similars.append(df_model1.iloc[id]["title"])
    return similars

def anime_score(user_input):
    # Return the anime score from the input
    df2 = pd.DataFrame([user_input], columns=use_cols)
    df_test = df_model1.append(df2, sort = True)

    X_test = df_test[use_cols].values
    x_test = preprocessing.StandardScaler().fit(X_test).transform(X_test.astype(float))
    score = neigh.predict([x_test[len(x_test) - 1]])
    return("The predicted anime score is: " + str(score))
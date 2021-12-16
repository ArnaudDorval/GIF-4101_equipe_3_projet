import numpy as np
from sklearn.feature_selection import mutual_info_classif, SelectKBest

from data import Data
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification

list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY']


#"step_variation", "hourly_variation",
#"mean", "none", min-max
data = Data(classification="hourly_variation",normalization="min-max")
X, y = data()
X_new = SelectKBest(mutual_info_classif, k=2).fit_transform(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_new, y, stratify=y,random_state=1)
clf = MLPClassifier(hidden_layer_sizes=(8, 8), activation='relu', solver='sgd', max_iter=500).fit(X_train, y_train)

clf.predict_proba(X_test)
print(clf.predict(X_test))

print(clf.score(X_test, y_test))
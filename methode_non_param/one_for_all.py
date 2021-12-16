import numpy as np
from data import Data
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, minmax_scale
from sklearn.multiclass import OneVsOneClassifier
from sklearn import svm
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.datasets import make_regression
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif

#list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY']
list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY', 'WEATHER']

#"step_variation", "hourly_variation",
#"mean", "none", min-max
data = Data(classification="hourly_variation",normalization="min-max")
X, y = data()

df = X
df['target'] = y
column_values = df[['target']].values
print(np.unique(column_values))

#X_new = SelectKBest(mutual_info_classif, k=3).fit_transform(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75)

m = OneVsOneClassifier(SVC(kernel='rbf'))

#print(m.classes_)
m.fit(X_train, y_train)

print(m.score(X_test, y_test))
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
import matplotlib.pyplot as plt

list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY']
#list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY', 'WEATHER', 'PREVIOUS']

#"step_variation", "hourly_variation",
#"mean", "none", min-max
data = Data(classification="hourly_variation",normalization="min-max")
X, y = data()

df = X.copy(deep=True)
df['target'] = y
column_values = df[['target']].values
print(np.unique(column_values))

list_int = ["0-25%", "25-50%", "50-75%", "75-100%", "100-125%", "125-150%", "150-175%"]
cls,  freq = np.unique(y, return_counts=True)
bars = plt.bar(data.y_explicite, np.array(freq) )  # density=False would make counts

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, yval)

plt.ylabel('Probability')
plt.xlabel('Classe')
plt.xticks(rotation=45, ha='right', labels=data.y_explicite, ticks=cls)

plt.title("Distribution du taux de variation de l'occupation")


plt.show()
my_count = pd.Series(y).value_counts()
print("count" + str(my_count[6]))

X_train, X_test, y_train, y_test = train_test_split(X[list_param], y, test_size=0.25)

m = OneVsOneClassifier(SVC(kernel='rbf'))

#print(m.classes_)
m.fit(X_train, y_train)

print(m.score(X_test, y_test))
t = m.predict(X_test)
print(t)

plt.hist(t)  # density=False would make counts
plt.ylabel('Probability')
plt.xlabel('Data')
plt.title("predict")

plt.show()
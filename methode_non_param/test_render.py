from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris
import numpy as np
from data import Data

#"step_variation", "hourly_variation",
#"mean", "none", min-max
data = Data(classification="hourly_variation",normalization="min-max")
x, y = data()

df = x
df['target'] = y
column_values = df[['target']].values
print(np.unique(column_values))

plt.close();
sns.set_style("whitegrid");
#, kind="hist"
sns.pairplot(df, hue="target", height=3);
plt.show()



print("ok")
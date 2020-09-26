import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
plt.style.use('ggplot')

data = pd.read_csv('data/train.csv')

X = data.iloc[:,:-1]
y = data.iloc[:,:1]

# Reduce dimensions
X_pca = PCA(n_components=2).fit_transform(X)

kf = KFold(n_splits=10)
kf.get_n_splits(X)

scores = []
best_score = np.inf

for k in range(1,30)[::2]:
    for train_index, val_index in kf.split(X):
        #X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        X_train, X_val = X_pca[train_index], X_pca[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]

        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train.values.ravel())

        preds = model.predict(X_val)
        rmse = mean_squared_error(preds, y_val)
        scores.append({
            'k': k,
            'RMSE': rmse,
        })
        if rmse < best_score:
            best_score = rmse
            print(k,rmse)


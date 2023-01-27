from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle 

df=pd.read_csv("diabetes.csv")

df.columns
y=df['Outcome']
x=df.drop(['Outcome'],axis=1)
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.1,random_state=42)
knn=KNeighborsClassifier(n_neighbors=15)
knn.fit(x_train.values,y_train)
X=[[8,65,72,23,0,32,0.6,42]]
#X= np.array(X)
print(X)
prdict=knn.predict(X)
print(prdict)

print(knn.score(x_test,y_test))

print(type(x_test))

import pickle 
  


filename = 'finalized_model.sav'
pickle.dump(knn, open(filename, 'wb'))

import pandas as pd

from sklearn.linear_model import LinearRegression

df=pd.read_csv("Advertising.csv")
df=df.iloc[:,1:len(df)]


x=df[["TV","radio","newspaper"]]

y=df[["sales"]]
reg=LinearRegression()
model=reg.fit(x,y)#modeli kur


print(model.predict([[230.1,37.8,69.2]]))
print("7.3+0.05*1")

import pickle

filename = "model.sav"
pickle.dump(model, open(filename, "wb"))


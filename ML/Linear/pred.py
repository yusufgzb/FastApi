import pickle

# Modeli geri yükle
model = pickle.load(open("model.sav", "rb"))

# Tahmin yap
example = [[230.1,37.8,69.2]]
prediction = model.predict(example)
print(prediction)

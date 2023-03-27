import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class PredictionInput(BaseModel):
    TV: float
    radio: float
    newspaper: float

@app.post("/predict")
def predict(predict_value: PredictionInput):
    # Yüklenen modeli aç
    filename = "model.sav"
    load_model = pickle.load(open(filename, "rb"))
    
    df = pd.DataFrame(
        [predict_value.dict().values()],
        columns=predict_value.dict().keys()
    )


    predict = load_model.predict(df)
    return {"Predict":int(predict[0])}


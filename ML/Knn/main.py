from fastapi import FastAPI, Path
import pickle
import pandas as pd

from pydantic import BaseModel


app = FastAPI()

class modelShema(BaseModel):
    Pregnancies:int
    Glucose:int
    BloodPressure:int
    SkinThickness:int
    Insulin:int
    BMI:float
    DiabetesPedigreeFunction:float
    Age:int

@app.get("/")
def hello():
    return {"hello": "hello world"}

@app.post("/predict/")
def create_student(predict_value: modelShema):
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    df = pd.DataFrame(
        [predict_value.dict().values()],
        columns=predict_value.dict().keys()
        )
    a=loaded_model.predict(df)
    return {"predict":int(a[0])}

# uvicorn main:app --reload

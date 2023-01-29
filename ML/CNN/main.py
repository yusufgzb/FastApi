from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_file 
from tensorflow.keras.utils import load_img 
from tensorflow.keras.utils import img_to_array
from tensorflow import expand_dims
from tensorflow.nn import softmax
from numpy import argmax
from numpy import max
from numpy import array
from json import dumps
from uvicorn import run
import os


app = FastAPI()


origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)

# Model dosyasını yüklüyoruz.
model_dir = "vision-model.h5"
model = load_model(model_dir)

# Tahmin edilebilecek sınıfları tanımlıyoruz.
class_predictions = array([
    'Fare',
    'Klavye',
    "Saat"
])

@app.get("/")
async def root():
    return {"message": "Welcome to the Vision API!"}


@app.post("/net/image/prediction/")
async def get_net_image_prediction(image_link: str = ""):
   
    if image_link == "":
        return {"message": "No image link provided"}
    
   
    img_path = get_file(
        origin = image_link
    )
   
  
    img = load_img(
        img_path, 
        target_size = (224, 224)
    )

    
    img_array = img_to_array(img)
    
    img_array = expand_dims(img_array, 0)

    
    pred = model.predict(img_array)

    score = softmax(pred[0])


    class_prediction = class_predictions[argmax(score)]

    model_score = round(max(score) * 100, 2)

    return {
        "model-prediction": class_prediction,
        "model-prediction-confidence-score": model_score
    }

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    
    run(app, host="0.0.0.0", port=port)

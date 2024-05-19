from typing import Union
import httpx
from fastapi import FastAPI
import json

app = FastAPI()

label_mapping = {
    0: {"name": "plastic", "nutrition": {"calories": 95, "fiber": 4.4, "sugar": 19}},
    1: {"name": "paper", "nutrition": {"calories": 105, "fiber": 3.1, "sugar": 14}},
    2: {"name": "organic", "nutrition": {"calories": 50, "fiber": 1.6, "sugar": 10}},
    3: {"name": "metal", "nutrition": {"calories": 282, "fiber": 8, "sugar": 63}},
    4: {"name": "glass", "nutrition": {"calories": 73, "fiber": 7, "sugar": 0}},
    5: {"name": "cardboard", "nutrition": {"calories": 74, "fiber": 2.9, "sugar": 16}}
}

@app.get("/")
def read_root():
    r = httpx.get('http://localhost:8601/v1/models/my_simple_model/versions/2')

    return r.json()

@app.post('/')
def predict():
    with open('plastic.json') as f:
        json_data = json.load(f)

    response = httpx.post('http://localhost:8601/v1/models/my_simple_model/versions/2:predict',
                   json=json_data)
    
    

    # Get the predictions from the response
    predictions = response.json().get('predictions', [])
    # predictions = response.json()

    translated_predictions = []

    for prediction in predictions:
        # Find the index of the maximum value in the prediction
        max_index = prediction.index(max(prediction))
        # Get the corresponding label from the label mapping
        translated_prediction = label_mapping[max_index]
        translated_predictions.append(translated_prediction)

    # # Translate numerical predictions to detailed labels
    # translated_predictions = []
    # for prediction in predictions:
    #     translated_prediction = []
    #     for i, value in enumerate(prediction):
    #         if value == 1.0:
    #             translated_prediction.append(label_mapping[i])
    #     translated_predictions.append(translated_prediction)
    
    # Return the translated predictions as JSON
    return {"translated_predictions": translated_predictions}
    # return {"translated_predictions": predictions}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
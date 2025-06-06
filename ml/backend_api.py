from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from ml.src.inference import ModelSelector

app = FastAPI()
selector = ModelSelector()

class PredictRequest(BaseModel):
    model_name: str
    input_data: list  # 2次元配列（サンプル数×特徴量数）

class PredictResponse(BaseModel):
    prediction: list

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # 入力データをnumpy配列に変換
    X = np.array(req.input_data)
    pred = selector.predict(req.model_name, X)
    return PredictResponse(prediction=pred) 
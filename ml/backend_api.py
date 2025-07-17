from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import traceback

app = FastAPI()

# ModelSelectorの初期化にエラーハンドリングを追加
try:
    from src.inference import ModelSelector
    selector = ModelSelector()
    print("ModelSelector initialized successfully")
except Exception as e:
    print(f"Error initializing ModelSelector: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    selector = None

class PredictRequest(BaseModel):
    model_name: str
    input_data: list  # 2次元配列（サンプル数×特徴量数）

class PredictResponse(BaseModel):
    prediction: list

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if selector is None:
        return PredictResponse(prediction=["Error: ModelSelector not initialized"])
    
    try:
        # 入力データをnumpy配列に変換
        X = np.array(req.input_data)
        pred = selector.predict(req.model_name, X)
        return PredictResponse(prediction=pred)
    except Exception as e:
        return PredictResponse(prediction=[f"Error: {str(e)}"]) 
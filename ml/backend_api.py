from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import traceback

app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 画像ファイル用のエンドポイントを追加
@app.post("/predict-image")
async def predict_image(
    task_name: str = Form(...),
    file: UploadFile = File(...)
):
    if selector is None:
        return {"error": "ModelSelector not initialized"}
    
    try:
        # ファイルの内容を読み込み
        contents = await file.read()
        
        # 手書き数字認識の場合
        if task_name == "handwritten_digit":
            result = selector.predict("handwritten_digit", contents)
            return {"prediction": result}
        else:
            return {"error": f"Unsupported task: {task_name}"}
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"} 
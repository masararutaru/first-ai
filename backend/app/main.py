from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# リクエストモデル
class PredictRequest(BaseModel):
    feature1: float
    feature2: Optional[float] = None
    confidence_threshold: Optional[float] = 0.8

# レスポンスモデル
class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    message: str

# FastAPI アプリの本体を作成
app = FastAPI(
    title="Machine Learning API",
    description="機械学習モデルの予測APIです",
    version="1.0.0"
)

# CORS設定を更新
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# ルートパス "/" に GET リクエストが来たときの処理を定義
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"こんにちは、{name}さん！"}

# POST で受け取る /predict エンドポイント
@app.post("/predict/{model_type}", response_model=PredictionResponse)
async def predict_post(model_type: str, req: PredictRequest):
    try:
        # ここを自分のモデル呼び出しに差し替えるだけで OK
        # prediction, confidence = your_model(req.feature1, req.feature2)
        prediction, confidence = 0.95, 0.9

        if confidence < req.confidence_threshold:
            raise HTTPException(status_code=400, detail="信頼度が低すぎます")

        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            message=f"{model_type} 予測完了"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"予測中にエラーが発生しました: {str(e)}"
        )
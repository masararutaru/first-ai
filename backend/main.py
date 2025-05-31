from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import sys
import os
from typing import Optional

# mlディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../ml')))
from src.inference import ModelSelector

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
selector = ModelSelector()

class PredictRequest(BaseModel):
    task_name: str
    input_data: Optional[object] = None

class PredictResponse(BaseModel):
    prediction: list

@app.post("/predict", response_model=PredictResponse)
async def predict(
    task_name: str = Form(None),
    input_data: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    body: Optional[PredictRequest] = None
):
    # 画像タスクはFormDataで受け取る
    if task_name == "image" and file is not None:
        # ここで画像ファイルを処理（ダミーなので未実装）
        pred = selector.predict(task_name, None)
        return PredictResponse(prediction=pred)
    # JSONリクエストの場合
    if body is not None:
        pred = selector.predict(body.task_name, body.input_data)
        return PredictResponse(prediction=pred)
    # フォールバック
    if task_name and input_data:
        import json
        pred = selector.predict(task_name, json.loads(input_data))
        return PredictResponse(prediction=pred)
    return PredictResponse(prediction=["入力が不正です"])

@app.get("/hello")
def read_hello():
    return {"message": "Hello from backend!"}

# エントリーポイントは不要（uvicornで直接appを指定するため）

# システムアーキテクチャ - first-ai

## 全体構成

```
┌─────────────────┐    HTTP     ┌─────────────────┐    Direct    ┌─────────────────┐
│   Frontend      │<----------->│    Backend      │<------------>│   ML Module     │
│   (Next.js)     │   8000      │   (FastAPI)     │   Import     │   (Python)      │
└─────────────────┘             └─────────────────┘              └─────────────────┘
```

## コンポーネント詳細

### フロントエンド（Next.js 15）
**場所**: `frontend/`
**技術スタック**:
- React 19 + TypeScript
- Tailwind CSS v4
- Next.js App Router

**主要ファイル**:
- `src/app/page.tsx`: メインUIコンポーネント
- `src/app/layout.tsx`: アプリケーションレイアウト
- `src/app/globals.css`: グローバルスタイル

**責務**:
- タスク選択UI提供
- 動的入力フォーム生成
- API通信とエラーハンドリング
- 結果の視覚的表示

### バックエンド（FastAPI）
**場所**: `backend/`
**技術スタック**:
- FastAPI + uvicorn
- Python 3.12
- Pydantic (データバリデーション)

**主要ファイル**:
- `main.py`: APIエンドポイント定義
- `pyproject.toml`: 依存関係管理

**責務**:
- RESTful API提供
- リクエスト形式の統一化
- CORS設定
- MLモジュールとの連携

### 機械学習モジュール
**場所**: `ml/`
**技術スタック**:
- scikit-learn
- joblib (モデル永続化)
- NumPy

**ディレクトリ構造**:
```
ml/
├── src/
│   ├── inference.py        # モデル統合インターフェース
│   └── models/            # 個別モデル格納
│       ├── sample_model/
│       └── sample_model2/
├── data/                  # データセット管理
├── config/               # 設定ファイル
└── requirements.txt      # Python依存関係
```

**責務**:
- モデルの読み込み・管理
- 推論実行
- 結果の標準化

## データフロー

### 1. 数値分類フロー
```
User Input → Frontend Validation → JSON Request → Backend → ModelSelector → 
scikit-learn Model → Prediction → JSON Response → Frontend Display
```

### 2. 画像分類フロー
```
User Upload → Frontend FormData → Multipart Request → Backend → ModelSelector → 
[Future: Image Model] → Prediction → JSON Response → Frontend Display
```

### 3. テキスト分類フロー
```
User Text → Frontend Validation → JSON Request → Backend → ModelSelector → 
[Future: NLP Model] → Prediction → JSON Response → Frontend Display
```

## 主要設計パターン

### 1. Strategy Pattern（モデル選択）
`ModelSelector` クラスが異なるタスクに対して適切なモデルを選択
```python
class ModelSelector:
    def predict(self, task_name: str, input_data):
        # タスクに応じたモデル選択ロジック
```

### 2. Factory Pattern（UI生成）
フロントエンドでタスクタイプに応じた入力コンポーネントを動的生成

### 3. Adapter Pattern（API統一）
異なる入力形式（JSON, FormData）を統一APIで処理

## 技術的決定事項

### フレームワーク選択理由
- **Next.js**: React基盤でSSR/SSG対応、開発生産性
- **FastAPI**: 自動ドキュメント生成、型安全性、高性能
- **scikit-learn**: 軽量、豊富なアルゴリズム、Kaggle互換性

### ディレクトリ分離設計
- **独立開発**: 各モジュールが独立してテスト・開発可能
- **スケーラビリティ**: チーム開発時の責任分界が明確
- **再利用性**: MLモジュールは他プロジェクトでも利用可能

### モデル管理方式
- **joblib永続化**: シンプルで高速な読み込み
- **ディレクトリ分離**: モデルごとの独立管理
- **設定外部化**: config/ での設定管理

## パフォーマンス考慮

### 現在の制約
- モデル読み込み: リクエスト毎（改善予定）
- ファイルアップロード: インメモリ処理のみ
- 同期処理: 並列リクエスト未対応

### 最適化計画
1. モデルの事前読み込み（メモリキャッシュ）
2. 非同期処理対応
3. ファイルストレージ統合
4. 負荷分散対応

## セキュリティ設計

### 現在の設定
- CORS: 開発用全許可設定
- 認証: 未実装
- ファイルバリデーション: 基本的な形式チェックのみ

### 本番対応予定
- CORS制限の適切な設定
- JWT認証の実装
- ファイルサイズ・形式の厳密バリデーション
- レート制限の実装 
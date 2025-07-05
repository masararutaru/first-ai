# 手書き数字認識モデル

## 概要
MNISTデータセットを使用した手書き数字（0-9）認識モデルです。

## モデル詳細
- **アルゴリズム**: MLPClassifier (多層パーセプトロン)
- **入力**: 28x28ピクセルのグレースケール画像（784次元ベクトル）
- **出力**: 0-9の数字クラス
- **データセット**: MNIST (Modified National Institute of Standards and Technology)

## 使用方法
```python
# モデルの学習・保存
python train_and_save.py

# 推論（inference.py経由）
from ml.src.inference import ModelSelector
selector = ModelSelector()
result = selector.predict('handwritten_digit', image_data)
```

## 入力形式
- 28x28ピクセルのグレースケール画像
- 値の範囲: 0-1（正規化済み）
- 1次元ベクトル（784要素）

## 出力形式
- 予測された数字（0-9）
- 確率スコア（オプション）

## 性能
- 学習データ: 10,000サンプル
- テストデータ: 2,000サンプル
- 期待精度: 95%以上 
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import joblib
import os

# ダミーデータ生成
X, y = make_classification(n_samples=100, n_features=4, random_state=42)

# モデル学習
model = LogisticRegression()
model.fit(X, y)

# 保存先ディレクトリ
save_dir = os.path.dirname(__file__)
model_path = os.path.join(save_dir, 'sample_model.joblib')

# モデル保存
joblib.dump(model, model_path)
print(f"モデルを保存しました: {model_path}") 
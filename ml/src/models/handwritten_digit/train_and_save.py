import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_mnist_model():
    """
    MNISTデータセットを使用して手書き数字認識モデルを学習・保存
    """
    print("MNISTデータセットを読み込み中...")
    
    # MNISTデータセットの取得
    mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
    X, y = mnist.data, mnist.target
    
    # データの前処理
    # 画像を28x28から1次元に変換済み、0-255の値を0-1に正規化
    X = X.astype('float32') / 255.0
    
    # データを分割（学習時間短縮のため一部のみ使用）
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # さらに学習時間短縮のため、サンプル数を制限
    X_train = X_train[:10000]  # 10000サンプル
    y_train = y_train[:10000]
    X_test = X_test[:2000]     # 2000サンプル
    y_test = y_test[:2000]
    
    print(f"学習データ: {X_train.shape}, テストデータ: {X_test.shape}")
    
    # モデルの学習
    print("モデルを学習中...")
    model = MLPClassifier(
        hidden_layer_sizes=(100, 50),  # 2層の隠れ層
        max_iter=300,
        random_state=42,
        verbose=True
    )
    
    model.fit(X_train, y_train)
    
    # モデルの評価
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"学習精度: {train_score:.4f}")
    print(f"テスト精度: {test_score:.4f}")
    
    # 保存先ディレクトリ
    save_dir = os.path.dirname(__file__)
    model_path = os.path.join(save_dir, 'mnist_model.joblib')
    
    # モデル保存
    joblib.dump(model, model_path)
    print(f"モデルを保存しました: {model_path}")
    
    return model, model_path

if __name__ == "__main__":
    train_mnist_model() 
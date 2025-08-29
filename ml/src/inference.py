import joblib
import numpy as np
import os
from PIL import Image
import io
import base64

class ModelSelector:
    """
    モデル選択用インターフェースクラスの雛形
    """
    def __init__(self):
        self.models = {
            'numeric': os.path.join(os.path.dirname(__file__), 'models', 'sample_model', 'sample_model.joblib'),
            'handwritten_digit': os.path.join(os.path.dirname(__file__), 'models', 'handwritten_digit', 'mnist_model.joblib'),
        }

    def _preprocess_image_for_mnist(self, image_data):
        """
        画像データをMNISTモデル用に前処理
        """
        # 画像データをPIL Imageに変換
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, str):
            image = Image.open(image_data)
        else:
            image = image_data
        
        # 元画像を保存（デバッグ用）
        original_image = image.copy()
        
        # グレースケールに変換
        if image.mode != 'L':
            image = image.convert('L')
        
        # 28x28にリサイズ
        image = image.resize((28, 28))
        
        # numpy配列に変換して正規化
        image_array = np.array(image, dtype='float32')
        
        # コントラストを改善（MNISTスタイルに近づける）
        # 白背景に黒文字の場合、反転して黒背景に白文字にする
        if np.mean(image_array) > 128:  # 背景が明るい場合
            image_array = 255 - image_array
        
        # 正規化
        image_array = image_array / 255.0
        
        # 1次元ベクトルに変換（784要素）
        image_vector = image_array.flatten()
        
        # デバッグ用画像をBase64エンコード
        debug_image = Image.fromarray((image_array * 255).astype(np.uint8))
        buffer = io.BytesIO()
        debug_image.save(buffer, format='PNG')
        debug_image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return image_vector.reshape(1, -1), debug_image_base64

    def predict(self, task_name: str, input_data):
        if task_name == 'numeric':
            model = joblib.load(self.models['numeric'])
            return model.predict(np.array(input_data)).tolist()
        elif task_name == 'handwritten_digit':
            # 手書き数字認識モデルの処理
            model = joblib.load(self.models['handwritten_digit'])
            processed_image, debug_image_base64 = self._preprocess_image_for_mnist(input_data)
            prediction = model.predict(processed_image)[0]
            probability = model.predict_proba(processed_image)[0]
            
            # デバッグ情報を追加
            debug_info = {
                'input_shape': processed_image.shape,
                'input_mean': float(np.mean(processed_image)),
                'input_std': float(np.std(processed_image)),
                'input_min': float(np.min(processed_image)),
                'input_max': float(np.max(processed_image))
            }
            
            return {
                'predicted_digit': int(prediction),
                'confidence': float(max(probability)),
                'probabilities': probability.tolist(),
                'debug_info': debug_info,
                'processed_image': debug_image_base64
            }
        elif task_name == 'image':
            # ここに画像分類モデルの処理を追加
            return ["画像分類ダミー結果"]
        elif task_name == 'text':
            # ここにテキスト分類モデルの処理を追加
            return ["テキスト分類ダミー結果"]
        else:
            raise ValueError(f"未対応のタスク名です: {task_name}") 
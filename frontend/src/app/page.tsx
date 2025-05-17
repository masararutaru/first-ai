'use client';

import { useState } from 'react';

interface PredictionResult {
  prediction: number;
  confidence: number;
  message: string;
}

export default function Home() {
  const [feature1, setFeature1] = useState<string>('');
  const [feature2, setFeature2] = useState<string>('');
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/predict/regression', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          feature1: parseFloat(feature1),
          feature2: feature2 ? parseFloat(feature2) : null,
        }),
      });

      if (!response.ok) {
        throw new Error('予測に失敗しました');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '予測中にエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">機械学習予測アプリ</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6 mb-8">
        <div>
          <label htmlFor="feature1" className="block text-sm font-medium mb-2">
            特徴量 1 (必須)
          </label>
          <input
            id="feature1"
            type="number"
            step="any"
            value={feature1}
            onChange={(e) => setFeature1(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-md"
            placeholder="例: 1.23"
          />
        </div>

        <div>
          <label htmlFor="feature2" className="block text-sm font-medium mb-2">
            特徴量 2 (オプション)
          </label>
          <input
            id="feature2"
            type="number"
            step="any"
            value={feature2}
            onChange={(e) => setFeature2(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            placeholder="例: 4.56"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !feature1}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-400"
        >
          {isLoading ? '予測中...' : '予測する'}
        </button>
      </form>

      {error && (
        <div className="p-4 bg-red-100 text-red-700 rounded-md mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="p-6 bg-green-50 rounded-md">
          <h2 className="text-xl font-semibold mb-4">予測結果</h2>
          <div className="space-y-2">
            <p>予測値: {result.prediction.toFixed(4)}</p>
            <p>信頼度: {(result.confidence * 100).toFixed(2)}%</p>
            <p className="text-gray-600">{result.message}</p>
          </div>
        </div>
      )}
    </main>
  );
}

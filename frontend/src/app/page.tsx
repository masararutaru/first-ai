"use client";
import Image from "next/image";
import { useState, ChangeEvent } from "react";

const TASKS = [
  { key: "numeric", label: "数値分類" },
  { key: "image", label: "画像分類" },
  { key: "text", label: "テキスト分類" },
];

export default function Home() {
  const [task, setTask] = useState("numeric");
  const [input, setInput] = useState("1.0,2.0,3.0,4.0");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [textInput, setTextInput] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const body: Record<string, unknown> = { task_name: task };
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      const url = "http://localhost:8000/predict";
      if (task === "numeric") {
        const inputArr = input
          .split("\n")
          .map((row) => row.split(",").map(Number));
        body.input_data = inputArr;
      } else if (task === "image") {
        // 画像はFormDataで送信
        const formData = new FormData();
        formData.append("task_name", task);
        if (imageFile) formData.append("file", imageFile);
        const res = await fetch(url, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        setResult(JSON.stringify(data.prediction));
        setLoading(false);
        return;
      } else if (task === "text") {
        body.input_data = textInput;
      }
      const res = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(body),
      });
      const data = await res.json();
      setResult(JSON.stringify(data.prediction));
    } catch (e) {
      setResult("エラー: " + e);
    }
    setLoading(false);
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <div className="flex flex-col gap-4 w-full max-w-md">
          <label htmlFor="task-select" className="font-bold">タスク選択</label>
          <select
            id="task-select"
            className="border rounded p-2 text-sm bg-white text-black focus:outline-blue-400"
            value={task}
            onChange={(e) => setTask(e.target.value)}
            style={{ minHeight: 40 }}
          >
            {TASKS.map((t) => (
              <option key={t.key} value={t.key}>{t.label}</option>
            ))}
          </select>
          {task === "numeric" && (
            <textarea
              className="border rounded p-2 text-sm"
              rows={3}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="1.0,2.0,3.0,4.0"
            />
          )}
          {task === "image" && (
            <input
              type="file"
              accept="image/*"
              className="border rounded p-2 text-sm"
              onChange={handleImageChange}
              aria-label="画像ファイルを選択"
            />
          )}
          {task === "text" && (
            <textarea
              className="border rounded p-2 text-sm"
              rows={3}
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="テキストを入力"
            />
          )}
          <button
            className="bg-blue-600 text-white rounded px-4 py-2 disabled:opacity-50"
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? "推論中..." : "推論する"}
          </button>
          {result && (
            <div className="mt-2 p-3 bg-blue-100 border border-blue-400 rounded text-base text-black font-bold text-center shadow">
              推論結果: {result}
            </div>
          )}
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

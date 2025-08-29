"use client";
import Image from "next/image";
import { useState, ChangeEvent } from "react";

const TASKS = [
  { key: "numeric", label: "数値分類" },
  { key: "image", label: "画像分類" },
  { key: "handwritten_digit", label: "手書き数字認識" },
  { key: "text", label: "テキスト分類" },
];

export default function Home() {
  const [task, setTask] = useState("numeric");
  const [input, setInput] = useState("1.0,2.0,3.0,4.0");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [textInput, setTextInput] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [processedImage, setProcessedImage] = useState<string | null>(null);

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    setProcessedImage(null);
    try {
      const body: Record<string, unknown> = { task_name: task };
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      const url = "http://localhost:8000/predict";
      if (task === "numeric") {
        const inputArr = input
          .split("\n")
          .map((row) => row.split(",").map(Number));
        body.input_data = inputArr;
      } else if (task === "image" || task === "handwritten_digit") {
        // 画像はFormDataで送信
        const formData = new FormData();
        formData.append("task_name", task);
        if (imageFile) formData.append("file", imageFile);
        const res = await fetch("http://localhost:8000/predict-image", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        
        // 手書き数字認識の場合は結果をシンプルに表示
        if (task === "handwritten_digit") {
          const prediction = data.prediction;
          setResult(`予測結果: ${prediction.predicted_digit}`);
          
          // 処理された画像を表示
          if (prediction.processed_image) {
            setProcessedImage(`data:image/png;base64,${prediction.processed_image}`);
          }
        } else {
          setResult(JSON.stringify(data.prediction));
        }
        
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
        <h1 className="text-4xl font-bold">Machine Learning</h1>
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
          {(task === "image" || task === "handwritten_digit") && (
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
          {processedImage && (
            <div className="mt-2 p-3 bg-gray-100 border border-gray-400 rounded">
              <h3 className="font-bold mb-2 text-black">モデルを適用した画像:</h3>
              <img 
                src={processedImage} 
                alt="Processed image" 
                className="border border-gray-300 rounded bg-white"
                style={{ 
                  imageRendering: 'pixelated',
                  filter: 'invert(1) contrast(3) brightness(0.8)'
                }}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

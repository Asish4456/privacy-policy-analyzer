import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzePolicy = async () => {
    if (!file && !text.trim()) {
      alert("Upload a PDF or paste policy text");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();

      if (file) {
        formData.append("file", file);
      } else {
        formData.append("text", text);
      }

      // ❌ DO NOT set Content-Type manually
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        formData
      );

      setResult(response.data);
    } catch (err) {
      alert("Failed to analyze policy");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card">

        <h1 className="title">Privacy Policy Analyzer</h1>
        <p className="subtitle">
          Upload a privacy policy or paste text to analyze privacy risks.
        </p>

        <div className="section">
          <label className="label">Upload PDF</label>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setText("");       // clear text when file selected
            }}
          />
        </div>

        <div className="divider">OR</div>

        <textarea
          placeholder="Paste privacy policy text here..."
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            setFile(null);       // clear file when typing
          }}
        />

        <button onClick={analyzePolicy} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Policy"}
        </button>

        {result && (
          <div className="result">
            <div
              className={`risk ${
                result.risk_level === "High"
                  ? "high"
                  : result.risk_level === "Medium"
                  ? "medium"
                  : "low"
              }`}
            >
              {result.risk_level} Risk
            </div>

            <p className="score">
              Risk Score: {result.risk_score} / 10
            </p>

            <progress value={result.risk_score} max="10"></progress>

            <ul>
              {result.insights.map((item, i) => (
                <li key={i}>{item[1]}</li>
              ))}
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;

import { useState } from "react";
import Video_form from "./components/Video_URL_Form";
import Output from "./components/Output";
import "./styles/App.css";

function App() {
  const [result, setResult] = useState(null);
  const [operation, setOperation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const processVideo = async (data) => {
    try {
      setLoading(true);
      setResult(null);
      setError(null);

      const response = await fetch(`${BASE_URL}/process`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const res = await response.json();

      if (res.status === "success") {
        setOperation(data.operation);

        const fileUrl = res.output_url.startsWith("http")
          ? res.output_url
          : `${BASE_URL}${res.output_url}`;

        setResult(fileUrl);
      } else {
        setError(res.message);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Media Processing Tool</h1>

      <div className="card">
        <Video_form onSubmit={processVideo} loading = {loading} />

        {loading && <p className="loading">Processing media, please wait...</p>}
        {error && <p className="error">{error}</p>}
      </div>

      {result && (
        <div className="card result-card">
          <h2>Result</h2>

          <Output result={result} operation={operation} />
        </div>
      )}
    </div>
  );
}

export default App;

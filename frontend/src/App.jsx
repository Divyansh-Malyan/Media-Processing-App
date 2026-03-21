import { useState } from "react";
import Video_form from "./components/Video_URL_Form";
import Output from "./components/Output";
import "./styles/App.css";

function App() {
  const [result, setResult] = useState(null);
  const [operation, setOperation] = useState(null);
  const [loading, setLoading] = useState(false);

  const BASE_URL = "http://localhost:8000";

  const processVideo = async (data) => {
    try {
      setLoading(true);
      setResult(null);

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
        alert(res.message);
      }
    } catch (err) {
      alert("API error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Media Processing Tool</h1>

      <div className="card">
        <Video_form onSubmit={processVideo} />

        {loading && <p className="loading">Processing media...</p>}
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

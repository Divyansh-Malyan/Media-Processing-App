import { useState } from "react";
import "../styles/Video_form.css";

function Video_URL_Form({ onSubmit }) {

  const [url, setUrl] = useState("");
  const [operation, setOperation] = useState("thumbnail");
  const [quality, setQuality] = useState("medium");
  const [bitrate, setBitrate] = useState("128");

  const handleSubmit = () => {
    if (!url) {
      alert("Please enter a media URL");
      return;
    }

    const data = {
      url,
      operation
    };

    if (operation === "compress") {
      data.quality = quality;
    }

    if (operation === "extract_audio") {
      data.bitrate = bitrate;
    }

    onSubmit(data);
  };

  return (

    <div className="form-container">

      <input
        className="url-input"
        type="text"
        placeholder="Paste Media URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <select
        className="operation-select"
        value={operation}
        onChange={(e) => setOperation(e.target.value)}
      >
        <option value="thumbnail">Thumbnail</option>
        <option value="compress">Compress</option>
        <option value="extract_audio">Extract Audio</option>
      </select>

      {operation === "compress" && (
        <select
          className="quality-select"
          value={quality}
          onChange={(e) => setQuality(e.target.value)}
        >
          <option value="low">Low (~small size)</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      )}

      {operation === "extract_audio" && (
        <select
          className="quality-select"
          value={bitrate}
          onChange={(e) => setBitrate(e.target.value)}
        >
          <option value="64">64 kbps</option>
          <option value="128">128 kbps</option>
          <option value="320">320 kbps</option>
        </select>
      )}

      <button
        className="process-btn"
        onClick={handleSubmit}
        disabled={!url}
      >
        {url ? "Process Media" : "Enter URL first"}
      </button>

    </div>

  );
}

export default Video_URL_Form;
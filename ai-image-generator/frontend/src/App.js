import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/generate/", {
        prompt: prompt,
      });

      console.log("API Response:", response.data);
      setImage(response.data.image_url);
    } catch (error) {
      console.error("Error generating image:", error);
    }
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Automotive Ai</h1>
      <h3>Generate your car ideas</h3>
      <input
        type="text"
        placeholder="Enter prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={generateImage} disabled={loading}>
        {loading ? "Generating..." : "Generate"}
      </button>

      {image && (
        <div>
          <h3>Generated Model:</h3>
          <img src={image} alt="Generated" width="400px" />
          <br />
          <a href={image} download="generated_image.png">
            <button>Download</button>
          </a>
        </div>
      )}
    </div>
  );
}

export default App;



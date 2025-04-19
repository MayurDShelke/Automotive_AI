import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState("");

  const generateImage = async () => {
    try {
      const formData = new FormData();
      formData.append("prompt", prompt);

      const response = await axios.post("http://localhost:8000/generate/", formData);
      setImage(`http://localhost:8000/image/${response.data.image_url}`);
    } catch (error) {
      console.error("Error generating image:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>AI Image Generator</h2>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt"
      />
      <button onClick={generateImage}>Generate</button>

      {image && <img src={image} alt="Generated" style={{ marginTop: "20px", maxWidth: "100%" }} />}
    </div>
  );
}

export default App;

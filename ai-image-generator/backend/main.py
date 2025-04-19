from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change if React runs on a different port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model_id = "dreamlike-art/dreamlike-diffusion-1.0"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, use_safetensors=True)
pipe = pipe.to("cuda")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate/")
async def generate_image(request: PromptRequest):
    try:
        # Generate image
        image = pipe(request.prompt).images[0]
        image_path = "generated_image.png"
        image.save(image_path)

        full_image_url = "http://127.0.0.1:8000/generated_image.png"
        print(f"✅ Image generated successfully: {full_image_url}")

        return {"image_url": full_image_url}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to serve the image
from fastapi.responses import FileResponse
import os

@app.get("/generated_image.png")
async def get_image():
    image_path = "generated_image.png"
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Image not found")

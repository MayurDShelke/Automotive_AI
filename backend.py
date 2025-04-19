import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch

app = FastAPI()

# CORS Middleware (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static folder if it doesn't exist
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")


# AI Model Loading
model_id = "dreamlike-art/dreamlike-diffusion-1.0"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.to("cuda")


class ImageRequest(BaseModel):
    prompt: str


@app.post("/generate/")
async def generate_image(request: ImageRequest):
    try:
        prompt = request.prompt
        image = pipe(prompt).images[0]

        # Save the generated image
        image_path = "static/generated_image.png"
        image.save(image_path)

        # Debugging: Check if file is saved
        if not os.path.exists(image_path):
            raise HTTPException(status_code=500, detail="Image not saved correctly")

        # Return the image URL
        return {"image_url": f"http://127.0.0.1:8000/static/generated_image.png"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


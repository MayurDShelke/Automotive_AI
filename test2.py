from diffusers import StableDiffusionPipeline
import torch
import matplotlib.pyplot as plt

# Model ID
model_id1 = "dreamlike-art/dreamlike-diffusion-1.0"
model_id2 = "stabilityai/stable-diffusion-xl-base-1.0"

# Load the pipeline
pipe = StableDiffusionPipeline.from_pretrained(model_id1, torch_dtype=torch.float16, use_safetensors=True)

# Move to GPU
pipe = pipe.to("cuda")

# Define prompt
prompt = input("Enter your image description: ")

# Generate image
image = pipe(prompt).images[0]

# Display image
plt.imshow(image)
plt.axis("off")
plt.show()

# Save image
image.save("output.png")

print("Image generated and saved as output.png!")


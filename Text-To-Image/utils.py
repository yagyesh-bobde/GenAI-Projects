from diffusers import StableDiffusionPipeline
import torch
def generate_image_with_diffusers(input_text):
    pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    pipeline = pipeline.to("cuda")
    prompt = input_text
    image = pipeline(prompt).images[0] 
    return image
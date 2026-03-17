---
name: diffusers-workflow
description: Use this skill when working with diffusion models for image/video generation. Covers Diffusers library pipelines, custom samplers, ControlNet, model training, and optimization techniques.
---

# Diffusers Workflow

This skill provides comprehensive guidance for working with diffusion models using the Hugging Face Diffusers library.

## When to Activate

- Generating images with Stable Diffusion
- Training diffusion models
- Implementing custom samplers
- Using ControlNet or IP-Adapter
- Video generation with diffusion
- Model distillation and optimization

## Pipeline Usage

### Basic Image Generation

```python
from diffusers import StableDiffusionXLPipeline
import torch

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")

# Enable memory optimization
pipe.enable_model_cpu_offload()

# Generate image
image = pipe(
    prompt="A majestic lion in the savanna at sunset",
    negative_prompt="blurry, low quality",
    num_inference_steps=30,
    guidance_scale=7.5,
).images[0]

image.save("lion.png")
```

### With LoRA

```python
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

# Load LoRA weights
pipe.load_lora_weights("path/to/lora", weight_name="lora.safetensors")

# Adjust LoRA scale
pipe.fuse_lora(lora_scale=0.8)

image = pipe("A portrait in the style of <lora_trigger>").images[0]
```

## ControlNet

### Basic ControlNet

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
import cv2
import numpy as np

# Load ControlNet
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16,
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16,
).to("cuda")

# Prepare control image (Canny edges)
image = load_image("input.png")
image = np.array(image)
edges = cv2.Canny(image, 100, 200)
control_image = Image.fromarray(edges)

# Generate with control
output = pipe(
    prompt="A detailed architectural drawing",
    image=control_image,
    num_inference_steps=30,
).images[0]
```

### Multi-ControlNet

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

# Load multiple ControlNets
controlnets = [
    ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny"),
    ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-depth"),
]

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnets,
    torch_dtype=torch.float16,
).to("cuda")

# Generate with multiple controls
output = pipe(
    prompt="A beautiful landscape",
    image=[canny_image, depth_image],
    controlnet_conditioning_scale=[1.0, 0.5],
).images[0]
```

## IP-Adapter

```python
from diffusers import StableDiffusionPipeline
from diffusers.utils import load_image

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

# Load IP-Adapter
pipe.load_ip_adapter("h94/IP-Adapter", subfolder="models", weight_name="ip-adapter_sd15.bin")

# Set adapter scale
pipe.set_ip_adapter_scale(0.6)

# Use reference image
ref_image = load_image("reference.png")
output = pipe(
    prompt="A person in a different setting",
    ip_adapter_image=ref_image,
).images[0]
```

## Custom Samplers

### Using Different Schedulers

```python
from diffusers import (
    DDPMScheduler,
    DDIMScheduler,
    EulerDiscreteScheduler,
    DPMSolverMultistepScheduler,
)

# Change scheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

# Or use Euler
pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config
)
```

### Custom Sampling Loop

```python
from diffusers import DDIMScheduler
import torch

def custom_sample(
    pipe,
    prompt,
    num_steps=50,
    guidance_scale=7.5,
):
    # Encode prompt
    prompt_embeds = pipe.encode_prompt(prompt, device=pipe.device, num_images_per_prompt=1)

    # Initialize latents
    latents = torch.randn(1, 4, 64, 64, device=pipe.device, dtype=torch.float16)
    latents = latents * pipe.scheduler.init_noise_sigma

    # Set timesteps
    pipe.scheduler.set_timesteps(num_steps)

    # Denoising loop
    for t in pipe.scheduler.timesteps:
        # Expand latents for classifier-free guidance
        latent_model_input = torch.cat([latents] * 2)
        latent_model_input = pipe.scheduler.scale_model_input(latent_model_input, t)

        # Predict noise
        with torch.no_grad():
            noise_pred = pipe.unet(
                latent_model_input,
                t,
                encoder_hidden_states=prompt_embeds,
            ).sample

        # Classifier-free guidance
        noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
        noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

        # Denoise
        latents = pipe.scheduler.step(noise_pred, t, latents).prev_sample

    # Decode
    image = pipe.vae.decode(latents / pipe.vae.config.scaling_factor).sample
    return image
```

## Training Diffusion Models

### Training UNet

```python
from diffusers import UNet2DConditionModel, DDPMScheduler
from diffusers.optimization import get_cosine_schedule_with_warmup
import torch.nn.functional as F

# Initialize model
unet = UNet2DConditionModel(
    sample_size=64,
    in_channels=4,
    out_channels=4,
    layers_per_block=2,
    block_out_channels=(320, 640, 1280, 1280),
    down_block_types=(
        "CrossAttnDownBlock2D",
        "CrossAttnDownBlock2D",
        "CrossAttnDownBlock2D",
        "DownBlock2D",
    ),
    up_block_types=(
        "UpBlock2D",
        "CrossAttnUpBlock2D",
        "CrossAttnUpBlock2D",
        "CrossAttnUpBlock2D",
    ),
    cross_attention_dim=768,
)

noise_scheduler = DDPMScheduler(num_train_timesteps=1000)

def train_step(model, batch, noise_scheduler):
    clean_images = batch["latents"]
    text_embeddings = batch["text_embeddings"]

    # Sample noise
    noise = torch.randn_like(clean_images)

    # Sample random timesteps
    timesteps = torch.randint(
        0, noise_scheduler.num_train_timesteps,
        (clean_images.shape[0],),
        device=clean_images.device
    )

    # Add noise to images
    noisy_images = noise_scheduler.add_noise(clean_images, noise, timesteps)

    # Predict noise
    noise_pred = model(noisy_images, timesteps, text_embeddings).sample

    # MSE loss
    loss = F.mse_loss(noise_pred, noise)

    return loss
```

### Fine-tuning with DreamBooth

```python
from diffusers import DiffusionPipeline, DDPMScheduler
from diffusers.loaders import AttnProcsLayers
from diffusers.models.attention_processor import LoRAAttnProcessor

# Load pipeline
pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
)

# Add LoRA layers
lora_attn_procs = {}
for name in pipe.unet.attn_processors.keys():
    lora_attn_procs[name] = LoRAAttnProcessor(
        hidden_size=pipe.unet.config.attention_head_dim,
        rank=4,
    )
pipe.unet.set_attn_processor(lora_attn_procs)

# Train only LoRA layers
lora_layers = AttnProcsLayers(pipe.unet.attn_processors)
optimizer = torch.optim.AdamW(lora_layers.parameters(), lr=1e-4)
```

## Video Generation

### AnimateDiff

```python
from diffusers import AnimateDiffPipeline, MotionAdapter, DDIMScheduler

# Load motion adapter
adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")

pipe = AnimateDiffPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    motion_adapter=adapter,
    torch_dtype=torch.float16,
).to("cuda")

pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

# Generate video
output = pipe(
    prompt="A cat walking on grass",
    num_frames=16,
    guidance_scale=7.5,
)

# Save as GIF
frames = output.frames[0]
frames[0].save("animation.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
```

## Memory Optimization

### CPU Offloading

```python
# Sequential CPU offload (slower but less memory)
pipe.enable_sequential_cpu_offload()

# Model CPU offload (faster, moderate memory)
pipe.enable_model_cpu_offload()

# Attention slicing
pipe.enable_attention_slicing()

# VAE slicing for large images
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
```

### xFormers Attention

```python
# Enable memory-efficient attention
pipe.enable_xformers_memory_efficient_attention()
```

### torch.compile

```python
# Compile for faster inference
pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)
```

## Image-to-Image

```python
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers.utils import load_image

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

init_image = load_image("input.png").resize((512, 512))

output = pipe(
    prompt="A fantasy landscape",
    image=init_image,
    strength=0.75,  # How much to transform
    guidance_scale=7.5,
).images[0]
```

## Inpainting

```python
from diffusers import StableDiffusionInpaintPipeline

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16,
).to("cuda")

init_image = load_image("image.png").resize((512, 512))
mask_image = load_image("mask.png").resize((512, 512))

output = pipe(
    prompt="A cat sitting on a couch",
    image=init_image,
    mask_image=mask_image,
).images[0]
```

## Best Practices

1. **Use fp16/bf16** for inference efficiency
2. **Enable xFormers** for memory optimization
3. **Use appropriate scheduler** for quality vs speed tradeoff
4. **Batch generation** when possible
5. **Seed control** for reproducibility
6. **Negative prompts** improve quality
7. **Guidance scale** between 7-12 typically works best
8. **Steps**: 20-50 depending on scheduler

## Common Issues

### Blurry outputs
- Increase guidance scale
- Use more steps
- Check VAE scaling factor

### Memory errors
- Enable CPU offload
- Reduce image size
- Use attention slicing

### Inconsistent style
- Fix random seed
- Use consistent prompts
- Apply LoRA for style

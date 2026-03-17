---
name: unified-generation
description: Use this skill when implementing unified understanding and generation models. Covers multi-task architectures, autoregressive vs diffusion approaches, multimodal tokenization, and next-token prediction paradigms.
---

# Unified Understanding and Generation

This skill provides guidance for implementing models that unify visual understanding and generation in a single framework.

## When to Activate

- Implementing unified vision-language models
- Designing multi-task architectures
- Choosing between autoregressive and diffusion approaches
- Working with multimodal tokenization
- Building systems that both understand and generate images

## Paradigm Overview

### Key Approaches

| Approach | Understanding | Generation | Examples |
|----------|---------------|------------|----------|
| **Separate Models** | CLIP + LLM | Diffusion | SD + LLaVA |
| **Unified AR** | Next-token | Next-token | Chameleon, Emu3 |
| **Unified Diffusion** | Encoder | Diffusion | DALL-E 3 |
| **Hybrid** | AR | AR + Diffusion | Show-o, Janus |

### Unified Autoregressive Approach

```
Text: "A cat on a sofa" → [text tokens] → Transformer → [image tokens] → Decoder → Image

Image: 🖼️ → Encoder → [image tokens] → Transformer → [text tokens] → "A cat on a sofa"
```

### Hybrid Approach (AR + Diffusion)

```
Understanding: Image → Visual Encoder → LLM → Text
Generation: Text → LLM → Diffusion Decoder → Image
```

## Visual Tokenization

### VQ-VAE / VQ-GAN Tokenizer

```python
class VQTokenizer(nn.Module):
    """Vector-quantized visual tokenizer."""

    def __init__(
        self,
        vocab_size: int = 16384,
        embed_dim: int = 256,
        img_size: int = 256,
        patch_size: int = 16,
    ):
        super().__init__()
        self.encoder = CNNEncoder(out_dim=embed_dim)
        self.decoder = CNNDecoder(in_dim=embed_dim)
        self.codebook = nn.Embedding(vocab_size, embed_dim)
        self.vocab_size = vocab_size

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Encode image to discrete tokens."""
        # x: (B, 3, H, W) -> z: (B, D, h, w)
        z = self.encoder(x)

        # Reshape for codebook lookup
        z = rearrange(z, 'b d h w -> b (h w) d')

        # Find nearest codebook entries
        distances = torch.cdist(z, self.codebook.weight)
        tokens = distances.argmin(dim=-1)  # (B, h*w)

        return tokens

    def decode(self, tokens: torch.Tensor) -> torch.Tensor:
        """Decode discrete tokens to image."""
        # tokens: (B, N) -> embeddings: (B, N, D)
        z = self.codebook(tokens)

        # Reshape and decode
        h = w = int(tokens.shape[1] ** 0.5)
        z = rearrange(z, 'b (h w) d -> b d h w', h=h, w=w)
        x = self.decoder(z)

        return x

    def tokenize_image(self, image: torch.Tensor) -> list[int]:
        """Convert image to token sequence."""
        tokens = self.encode(image)
        return tokens[0].tolist()

    def detokenize_image(self, tokens: list[int]) -> torch.Tensor:
        """Convert token sequence to image."""
        tokens = torch.tensor(tokens).unsqueeze(0)
        return self.decode(tokens)
```

### Continuous Visual Tokens (for diffusion)

```python
class ContinuousVisualEncoder(nn.Module):
    """Encode images to continuous visual tokens for LLM input."""

    def __init__(self, vision_model: str = "openai/clip-vit-large-patch14"):
        super().__init__()
        self.vision_encoder = CLIPVisionModel.from_pretrained(vision_model)
        self.projector = nn.Linear(1024, 4096)  # Project to LLM dim

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        """
        Args:
            images: (B, C, H, W) normalized images
        Returns:
            visual_tokens: (B, N, D) visual token embeddings
        """
        # Get patch features from CLIP
        vision_outputs = self.vision_encoder(images)
        patch_features = vision_outputs.last_hidden_state[:, 1:]  # Remove CLS

        # Project to LLM dimension
        visual_tokens = self.projector(patch_features)

        return visual_tokens
```

## Unified Architecture Design

### Unified Transformer for AR

```python
class UnifiedTransformer(nn.Module):
    """Single transformer for text and image generation via next-token prediction."""

    def __init__(
        self,
        text_vocab_size: int = 32000,
        image_vocab_size: int = 16384,
        hidden_size: int = 4096,
        num_layers: int = 32,
        num_heads: int = 32,
    ):
        super().__init__()

        # Unified vocabulary: [text tokens | image tokens | special tokens]
        total_vocab = text_vocab_size + image_vocab_size + 10
        self.embedding = nn.Embedding(total_vocab, hidden_size)

        # Transformer layers
        self.layers = nn.ModuleList([
            TransformerBlock(hidden_size, num_heads)
            for _ in range(num_layers)
        ])

        self.norm = nn.LayerNorm(hidden_size)
        self.lm_head = nn.Linear(hidden_size, total_vocab)

        # Special token IDs
        self.boi_token = text_vocab_size + image_vocab_size  # Begin of Image
        self.eoi_token = text_vocab_size + image_vocab_size + 1  # End of Image
        self.image_offset = text_vocab_size  # Offset for image tokens

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        # Embed tokens
        x = self.embedding(input_ids)

        # Apply transformer layers
        for layer in self.layers:
            x = layer(x, attention_mask)

        x = self.norm(x)
        logits = self.lm_head(x)

        return logits

    def generate_image(
        self,
        text_tokens: torch.Tensor,
        num_image_tokens: int = 256,
        temperature: float = 1.0,
        top_k: int = 100,
    ) -> torch.Tensor:
        """Generate image tokens autoregressively."""
        device = text_tokens.device

        # Start with text + BOI token
        boi = torch.tensor([[self.boi_token]], device=device)
        tokens = torch.cat([text_tokens, boi], dim=1)

        # Generate image tokens
        for _ in range(num_image_tokens):
            logits = self(tokens)
            next_logits = logits[:, -1, self.image_offset:self.image_offset + 16384]

            # Sample
            next_logits = next_logits / temperature
            if top_k > 0:
                v, _ = torch.topk(next_logits, top_k)
                next_logits[next_logits < v[:, [-1]]] = float('-inf')

            probs = F.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, 1) + self.image_offset
            tokens = torch.cat([tokens, next_token], dim=1)

        # Add EOI token
        eoi = torch.tensor([[self.eoi_token]], device=device)
        tokens = torch.cat([tokens, eoi], dim=1)

        return tokens[:, -num_image_tokens-1:-1] - self.image_offset
```

### Hybrid Architecture (Show-o / Janus style)

```python
class HybridUnifiedModel(nn.Module):
    """
    Hybrid model: AR for understanding, AR+Diffusion for generation.
    Based on Show-o / Janus architectures.
    """

    def __init__(
        self,
        llm_config: dict,
        vision_encoder_config: dict,
        diffusion_config: dict,
    ):
        super().__init__()

        # Vision encoder for understanding
        self.vision_encoder = SigLIPVisionEncoder(**vision_encoder_config)

        # LLM backbone
        self.llm = LlamaForCausalLM.from_pretrained(llm_config["model_name"])

        # Projectors
        self.vision_projector = nn.Linear(
            vision_encoder_config["hidden_size"],
            llm_config["hidden_size"]
        )

        # Diffusion head for generation
        self.diffusion_head = DiffusionDecoder(**diffusion_config)

        # Adapter to convert LLM hidden states to diffusion conditioning
        self.generation_adapter = nn.Sequential(
            nn.Linear(llm_config["hidden_size"], diffusion_config["cond_dim"]),
            nn.SiLU(),
            nn.Linear(diffusion_config["cond_dim"], diffusion_config["cond_dim"]),
        )

    def understand(
        self,
        images: torch.Tensor,
        text_input_ids: torch.Tensor,
    ) -> torch.Tensor:
        """Image understanding via visual QA."""
        # Encode images
        visual_features = self.vision_encoder(images)
        visual_tokens = self.vision_projector(visual_features)

        # Get text embeddings
        text_embeds = self.llm.get_input_embeddings()(text_input_ids)

        # Concatenate visual and text tokens
        inputs_embeds = torch.cat([visual_tokens, text_embeds], dim=1)

        # Generate response
        outputs = self.llm.generate(
            inputs_embeds=inputs_embeds,
            max_new_tokens=512,
        )

        return outputs

    def generate(
        self,
        text_input_ids: torch.Tensor,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> torch.Tensor:
        """Image generation from text."""
        # Get LLM hidden states for text
        outputs = self.llm(
            input_ids=text_input_ids,
            output_hidden_states=True,
        )
        hidden_states = outputs.hidden_states[-1]

        # Convert to diffusion conditioning
        conditioning = self.generation_adapter(hidden_states)

        # Generate image via diffusion
        image = self.diffusion_head.sample(
            conditioning=conditioning,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        )

        return image
```

## Training Strategies

### Multi-Task Training

```python
class UnifiedTrainer:
    """Trainer for unified understanding and generation."""

    def __init__(self, model, optimizer):
        self.model = model
        self.optimizer = optimizer

    def train_step(self, batch):
        """Single training step with mixed tasks."""
        task_type = batch["task_type"]

        if task_type == "text":
            # Standard language modeling
            loss = self.text_loss(batch)

        elif task_type == "understanding":
            # Image -> Text (VQA, captioning)
            loss = self.understanding_loss(batch)

        elif task_type == "generation":
            # Text -> Image
            loss = self.generation_loss(batch)

        elif task_type == "interleaved":
            # Mixed text and image sequence
            loss = self.interleaved_loss(batch)

        return loss

    def text_loss(self, batch):
        """Standard next-token prediction for text."""
        logits = self.model(batch["input_ids"])
        loss = F.cross_entropy(
            logits[:, :-1].reshape(-1, logits.size(-1)),
            batch["input_ids"][:, 1:].reshape(-1),
        )
        return loss

    def understanding_loss(self, batch):
        """Visual understanding loss."""
        # Image tokens + text tokens -> next text token
        combined_ids = torch.cat([
            batch["image_tokens"] + self.model.image_offset,
            batch["text_ids"],
        ], dim=1)

        logits = self.model(combined_ids)

        # Only compute loss on text portion
        text_logits = logits[:, batch["image_tokens"].size(1):-1]
        text_targets = batch["text_ids"][:, 1:]

        loss = F.cross_entropy(
            text_logits.reshape(-1, text_logits.size(-1)),
            text_targets.reshape(-1),
        )
        return loss

    def generation_loss(self, batch):
        """Image generation loss."""
        # Text tokens + image tokens -> next image token
        combined_ids = torch.cat([
            batch["text_ids"],
            batch["image_tokens"] + self.model.image_offset,
        ], dim=1)

        logits = self.model(combined_ids)

        # Only compute loss on image portion
        image_logits = logits[:, batch["text_ids"].size(1):-1]
        image_targets = batch["image_tokens"][:, 1:]

        # Mask to only predict image tokens
        loss = F.cross_entropy(
            image_logits.reshape(-1, image_logits.size(-1)),
            (image_targets + self.model.image_offset).reshape(-1),
        )
        return loss
```

### Loss Balancing

```python
class AdaptiveLossBalancer:
    """Dynamically balance losses across tasks."""

    def __init__(self, task_names: list[str], init_weights: dict = None):
        self.task_names = task_names
        self.log_vars = nn.ParameterDict({
            name: nn.Parameter(torch.zeros(1))
            for name in task_names
        })

    def __call__(self, losses: dict[str, torch.Tensor]) -> torch.Tensor:
        """Compute weighted sum with uncertainty weighting."""
        total_loss = 0
        for name in self.task_names:
            if name in losses:
                precision = torch.exp(-self.log_vars[name])
                total_loss += precision * losses[name] + self.log_vars[name]
        return total_loss
```

## Evaluation

### Understanding Metrics

```python
def evaluate_understanding(model, dataset):
    """Evaluate visual understanding capabilities."""
    metrics = {
        "vqa_accuracy": evaluate_vqa(model, dataset["vqa"]),
        "caption_cider": evaluate_captioning(model, dataset["coco"]),
        "ocr_accuracy": evaluate_ocr(model, dataset["textvqa"]),
    }
    return metrics
```

### Generation Metrics

```python
def evaluate_generation(model, dataset):
    """Evaluate image generation capabilities."""
    generated_images = []
    for prompt in dataset["prompts"]:
        image = model.generate(prompt)
        generated_images.append(image)

    metrics = {
        "fid": compute_fid(generated_images, dataset["real_images"]),
        "clip_score": compute_clip_score(generated_images, dataset["prompts"]),
        "aesthetic_score": compute_aesthetic_score(generated_images),
    }
    return metrics
```

## Best Practices

1. **Start with pretrained components** - Use pretrained LLM and visual encoder
2. **Progressive training** - Train understanding first, then add generation
3. **Balance task ratios** - Prevent one task from dominating
4. **Use task-specific tokens** - Clear boundaries between modalities
5. **Quality visual tokenizer** - Generation quality depends heavily on this
6. **Evaluate both capabilities** - Don't neglect understanding for generation

## Related Work

- **Chameleon** (Meta): Fully AR unified model
- **Emu/Emu2** (BAAI): Multimodal understanding + generation
- **Show-o**: Unified with omni-attention
- **Janus** (DeepSeek): Decoupled visual encoding
- **Transfusion**: Mix AR and diffusion in one forward pass

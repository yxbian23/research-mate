---
description: Implement research papers - extract algorithms from arXiv papers, translate formulas to PyTorch, generate code frameworks, and verify correctness.
---

# Implement Paper Command

This command systematically implements algorithms and models from research papers.

## What This Command Does

1. **Parse Paper** - Extract key algorithms and formulas
2. **Analyze Architecture** - Understand model structure
3. **Generate Code** - Translate to PyTorch implementation
4. **Verify Correctness** - Test against paper's results

## When to Use

Use `/implement-paper` when:
- Implementing a model from a new paper
- Translating mathematical formulas to code
- Reproducing paper results
- Understanding complex architectures

## Implementation Workflow

### Phase 1: Paper Analysis
- Extract core contributions
- Identify key equations
- Note hyperparameters
- Find reference implementations

### Phase 2: Code Structure
- Design class hierarchy
- Define interfaces
- Plan testing strategy

### Phase 3: Implementation
- Implement core components
- Add shape assertions
- Include docstrings with formulas

### Phase 4: Verification
- Unit test each component
- Compare with reference (if available)
- Validate on toy data

## Example Usage

```
User: /implement-paper https://arxiv.org/abs/2212.09748

Agent:
# Paper Implementation Plan

## Paper: DiT - Scalable Diffusion Models with Transformers
**arXiv**: 2212.09748
**Authors**: Peebles & Xie (Meta AI)

## Key Contributions
1. Replace U-Net backbone with Vision Transformer
2. Adaptive Layer Normalization (adaLN-Zero)
3. Scaling analysis of diffusion transformers

## Core Components to Implement

### 1. DiT Block (Equation 1-3)
```python
class DiTBlock(nn.Module):
    """
    DiT block with adaLN-Zero conditioning.

    Equations:
    - γ₁, β₁, α₁, γ₂, β₂, α₂ = MLP(t_embed)
    - x = x + α₁ * Attention(adaLN(x, γ₁, β₁))
    - x = x + α₂ * MLP(adaLN(x, γ₂, β₂))
    """
    def __init__(self, hidden_size, num_heads):
        super().__init__()
        self.norm1 = nn.LayerNorm(hidden_size, elementwise_affine=False)
        self.attn = Attention(hidden_size, num_heads)
        self.norm2 = nn.LayerNorm(hidden_size, elementwise_affine=False)
        self.mlp = MLP(hidden_size)
        self.adaLN_modulation = nn.Sequential(
            nn.SiLU(),
            nn.Linear(hidden_size, 6 * hidden_size)
        )

    def forward(self, x, c):
        shift_msa, scale_msa, gate_msa, shift_mlp, scale_mlp, gate_mlp = \
            self.adaLN_modulation(c).chunk(6, dim=-1)

        x = x + gate_msa * self.attn(modulate(self.norm1(x), shift_msa, scale_msa))
        x = x + gate_mlp * self.mlp(modulate(self.norm2(x), shift_mlp, scale_mlp))
        return x
```

### 2. Patchify Layer
```python
class PatchEmbed(nn.Module):
    """Convert image to patches with position embedding."""
    def __init__(self, img_size=256, patch_size=2, in_channels=4, embed_dim=1152):
        super().__init__()
        self.proj = nn.Conv2d(in_channels, embed_dim, patch_size, patch_size)
        self.num_patches = (img_size // patch_size) ** 2

    def forward(self, x):
        return self.proj(x).flatten(2).transpose(1, 2)
```

### 3. Time Embedding
```python
class TimestepEmbedder(nn.Module):
    """Sinusoidal timestep embeddings."""
    def __init__(self, hidden_size, freq_embed_size=256):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(freq_embed_size, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size),
        )
        self.freq_embed_size = freq_embed_size

    def forward(self, t):
        freq = timestep_embedding(t, self.freq_embed_size)
        return self.mlp(freq)
```

## Hyperparameters (Table 1)
| Model | Layers | Hidden | Heads | Params |
|-------|--------|--------|-------|--------|
| DiT-S | 12 | 384 | 6 | 33M |
| DiT-B | 12 | 768 | 12 | 130M |
| DiT-L | 24 | 1024 | 16 | 458M |
| DiT-XL | 28 | 1152 | 16 | 675M |

## Verification Plan
1. Compare parameter count with paper
2. Check output shapes match
3. Verify adaLN conditioning
4. Test on CIFAR-10 before ImageNet

**Proceed with implementation?** (yes/no/modify)
```

## Paper Reading Tips

### Where to Find Key Info
- **Architecture**: Method section, Figure 1
- **Hyperparameters**: Section 4 or Appendix
- **Training details**: Section 4.1 or Appendix A
- **Ablations**: Section 4.2 or Appendix B

### Common Notation
| Symbol | Meaning |
|--------|---------|
| x | Input/hidden state |
| t | Timestep |
| c | Conditioning signal |
| γ, β | Scale and shift |
| α | Gate/residual scale |

## Implementation Checklist

- [ ] Core model architecture
- [ ] Loss function
- [ ] Training loop
- [ ] Sampling/inference
- [ ] Evaluation metrics
- [ ] Config matching paper

## Related Commands

- `/analyze-paper` - Deep analysis without implementation
- `/train` - Train the implemented model
- `/eval-model` - Evaluate implementation
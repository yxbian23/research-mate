# Security Guidelines (ML Research)

## Mandatory Security Checks

Before ANY commit:
- [ ] No hardcoded secrets (API keys, HF tokens, wandb keys)
- [ ] No credentials in config files
- [ ] Model weights excluded from git
- [ ] Sensitive data paths not exposed
- [ ] .env files gitignored

## Secret Management

```python
# NEVER: Hardcoded secrets
api_key = "sk-proj-xxxxx"
hf_token = "hf_..."

# ALWAYS: Environment variables
import os
api_key = os.environ.get("OPENAI_API_KEY")
hf_token = os.environ.get("HF_TOKEN")

if not api_key:
    raise ValueError("OPENAI_API_KEY not configured")
```

## Config File Security

```yaml
# config.yaml - Safe to commit
model:
  name: llama-7b
  # Reference env vars, don't hardcode
  hub_token: ${HF_TOKEN}

training:
  wandb_project: my-project
  # API key from environment
```

## .gitignore Requirements

```gitignore
# Secrets
.env
*.pem
*credentials*
secrets.yaml

# Model weights (large files)
*.pt
*.pth
*.safetensors
*.ckpt
checkpoints/

# Experiment outputs
wandb/
outputs/
logs/

# Data
data/
*.parquet
*.arrow
```

## Safe Model Loading

```python
# For untrusted sources, use weights_only
model_dict = torch.load(path, weights_only=True)

# Or use safetensors (recommended)
from safetensors.torch import load_file
model_dict = load_file("model.safetensors")
```

## Security Response Protocol

If security issue found:
1. STOP immediately
2. Use **security-reviewer** agent
3. Fix CRITICAL issues before continuing
4. Rotate any exposed secrets
5. Review entire codebase for similar issues

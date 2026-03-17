# Performance Optimization

## Model Selection Strategy

**Haiku 4.5** (90% of Sonnet capability, 3x cost savings):
- Quick code reviews and simple fixes
- Lightweight debugging tasks
- Documentation updates
- Simple refactoring

**Sonnet 4.5** (Best coding model):
- Main development work
- Model implementation
- Training script development
- Complex debugging

**Opus 4.5** (Deepest reasoning):
- Complex architectural decisions
- Paper analysis and implementation planning
- Research and analysis tasks
- Multi-step problem solving

## Context Window Management

Avoid last 20% of context window for:
- Large model implementations
- Complex training pipelines
- Multi-file refactoring

Lower context sensitivity tasks:
- Single-file edits
- Config modifications
- Simple bug fixes
- Documentation updates

## Ultrathink + Plan Mode

For complex ML tasks requiring deep reasoning:
1. Use `ultrathink` for enhanced thinking
2. Enable **Plan Mode** for structured approach
3. "Rev the engine" with multiple critique rounds
4. Use split role sub-agents for diverse analysis

## ML Training Performance

### GPU Optimization Priority

1. **Enable mixed precision** (bf16/fp16)
2. **Enable gradient checkpointing** for large models
3. **Optimize batch size** with gradient accumulation
4. **Use efficient data loading** (num_workers, pin_memory)

### Memory Troubleshooting

If OOM error:
1. Check memory with `torch.cuda.memory_allocated()`
2. Enable gradient checkpointing
3. Reduce batch size
4. Try DeepSpeed/FSDP for large models

## Profiling First

ALWAYS profile before optimizing:

```python
# PyTorch profiler
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CUDA]) as prof:
    model(input)

print(prof.key_averages().table())
```

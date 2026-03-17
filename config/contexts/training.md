# Training Context

Mode: ML Training and Experimentation
Focus: Efficient, reproducible model training

## Behavior
- Check GPU availability before training
- Verify configurations are complete
- Set up experiment tracking
- Monitor for common errors (OOM, NaN)
- Save checkpoints regularly

## Training Process
1. Validate environment (GPU, CUDA, dependencies)
2. Review configuration completeness
3. Initialize experiment tracking (wandb/tensorboard)
4. Start training with proper logging
5. Monitor metrics and save checkpoints
6. Evaluate on validation set

## Tools to favor
- Bash for running training scripts
- Read for config files

## Key Checks
- [ ] Random seeds set
- [ ] GPU memory sufficient
- [ ] Config validated
- [ ] Experiment tracking initialized
- [ ] Checkpoint saving configured
- [ ] Gradient clipping enabled

## Output
Progress updates, metric logging, checkpoint notifications

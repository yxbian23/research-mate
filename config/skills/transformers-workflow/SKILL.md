---
name: transformers-workflow
description: Use this skill when working with Hugging Face Transformers library. Covers model loading, fine-tuning, LoRA/QLoRA adaptation, tokenizer usage, datasets processing, and Trainer API.
---

# Hugging Face Transformers Workflow

This skill provides comprehensive guidance for using the Hugging Face ecosystem for NLP and multimodal tasks.

## When to Activate

- Loading and using pretrained models
- Fine-tuning language models
- Applying LoRA/QLoRA for efficient training
- Processing datasets with the datasets library
- Using the Trainer API

## Model Loading Patterns

### Basic Model Loading

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
```

### Loading with Quantization

```python
from transformers import BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)
```

### Loading for Vision-Language Models

```python
from transformers import LlavaForConditionalGeneration, AutoProcessor

model = LlavaForConditionalGeneration.from_pretrained(
    "llava-hf/llava-1.5-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
```

## LoRA Fine-tuning

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Prepare model for training
model = prepare_model_for_kbit_training(model)

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,  # Alpha scaling
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.062
```

## QLoRA Training

```python
from transformers import TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=64,
    lora_alpha=128,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir="./output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    warmup_ratio=0.03,
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    bf16=True,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
)
```

## Tokenizer Usage

### Basic Tokenization

```python
# Tokenize text
text = "Hello, how are you?"
tokens = tokenizer(text, return_tensors="pt")
# Output: {'input_ids': tensor([[...]]), 'attention_mask': tensor([[...]])}

# Decode tokens
decoded = tokenizer.decode(tokens['input_ids'][0])
```

### Chat Template

```python
# Format chat messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

# Apply chat template
formatted = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

# Tokenize with chat template
inputs = tokenizer.apply_chat_template(
    messages,
    return_tensors="pt",
    add_generation_prompt=True,
)
```

### Handling Special Tokens

```python
# Set padding token (for models without one)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Add special tokens
special_tokens = {"additional_special_tokens": ["<image>", "</image>"]}
tokenizer.add_special_tokens(special_tokens)
model.resize_token_embeddings(len(tokenizer))
```

## Dataset Processing

### Loading Datasets

```python
from datasets import load_dataset, Dataset

# From Hugging Face Hub
dataset = load_dataset("tatsu-lab/alpaca")

# From local files
dataset = load_dataset("json", data_files="data.jsonl")

# From pandas
import pandas as pd
df = pd.read_csv("data.csv")
dataset = Dataset.from_pandas(df)
```

### Preprocessing for Training

```python
def preprocess_function(examples):
    """Format examples for instruction tuning."""
    prompts = []
    for instruction, input_text, output in zip(
        examples["instruction"],
        examples["input"],
        examples["output"]
    ):
        if input_text:
            prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
        else:
            prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
        prompts.append(prompt)

    # Tokenize
    tokenized = tokenizer(
        prompts,
        truncation=True,
        max_length=2048,
        padding=False,
    )

    # Set labels = input_ids for causal LM
    tokenized["labels"] = tokenized["input_ids"].copy()

    return tokenized

# Apply preprocessing
tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset.column_names,
    num_proc=4,
)
```

### Data Collator

```python
from transformers import DataCollatorForLanguageModeling

# For causal LM (mask labels where padding)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # Not masked LM
)
```

## Trainer API

### Basic Training

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_ratio=0.03,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    bf16=True,
    dataloader_num_workers=4,
    report_to="wandb",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()
```

### Custom Training Loop with Trainer

```python
from transformers import Trainer
import torch

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        """Custom loss computation."""
        outputs = model(**inputs)
        loss = outputs.loss

        # Add custom regularization
        l2_reg = sum(p.pow(2).sum() for p in model.parameters())
        loss = loss + 1e-5 * l2_reg

        return (loss, outputs) if return_outputs else loss

    def training_step(self, model, inputs, num_items_in_batch=None):
        """Custom training step."""
        model.train()
        inputs = self._prepare_inputs(inputs)

        with self.compute_loss_context_manager():
            loss = self.compute_loss(model, inputs)

        # Custom gradient handling
        self.accelerator.backward(loss)

        return loss.detach()
```

## Generation

### Basic Generation

```python
# Generate text
inputs = tokenizer("Once upon a time", return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Advanced Generation Settings

```python
from transformers import GenerationConfig

generation_config = GenerationConfig(
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    do_sample=True,
    repetition_penalty=1.1,
    no_repeat_ngram_size=3,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id,
)

outputs = model.generate(
    **inputs,
    generation_config=generation_config,
)
```

### Streaming Generation

```python
from transformers import TextStreamer

streamer = TextStreamer(tokenizer, skip_prompt=True)
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    streamer=streamer,
)
```

## Model Merging

### Merge LoRA Weights

```python
from peft import PeftModel

# Load base model and LoRA adapter
base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, lora_adapter_path)

# Merge weights
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("merged_model")
tokenizer.save_pretrained("merged_model")
```

## Best Practices

1. **Use gradient checkpointing** for large models
2. **Enable flash attention** when available
3. **Use bf16** over fp16 for stability
4. **Set proper padding** token for batch processing
5. **Use streaming** for memory-efficient data loading
6. **Save checkpoints** frequently during training
7. **Monitor with wandb** or tensorboard
8. **Test on small subset** before full training

## Common Issues

### Out of Memory
- Reduce batch size
- Enable gradient checkpointing
- Use gradient accumulation
- Try 4-bit quantization

### Training Instability
- Reduce learning rate
- Add warmup steps
- Use gradient clipping
- Check data quality

### Poor Generation
- Adjust temperature
- Try different top_p/top_k
- Check tokenizer settings
- Verify model loaded correctly

---
name: dataset-processing
description: Use this skill when processing large-scale ML datasets. Covers data loading, preprocessing, augmentation, multimodal data handling, and streaming/sharding techniques.
---

# Dataset Processing

This skill provides comprehensive guidance for processing and managing large-scale machine learning datasets.

## When to Activate

- Loading and preprocessing large datasets
- Creating custom data pipelines
- Implementing data augmentation
- Processing multimodal data (image+text)
- Setting up distributed data loading

## Data Loading Patterns

### Basic PyTorch DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data_path: str, transform=None):
        self.data = self._load_data(data_path)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        if self.transform:
            item = self.transform(item)
        return item

# DataLoader with optimal settings
dataloader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
    prefetch_factor=2,
    persistent_workers=True,
)
```

### HuggingFace Datasets

```python
from datasets import load_dataset, Dataset, DatasetDict

# Load from Hub
dataset = load_dataset("imagenet-1k", split="train")

# Load from local files
dataset = load_dataset("json", data_files="data.jsonl")
dataset = load_dataset("csv", data_files="data.csv")
dataset = load_dataset("parquet", data_files="data.parquet")

# Load from folder structure
dataset = load_dataset("imagefolder", data_dir="images/")

# Create from pandas
import pandas as pd
df = pd.read_csv("data.csv")
dataset = Dataset.from_pandas(df)
```

### WebDataset for Large-Scale Data

```python
import webdataset as wds

# Create WebDataset from sharded tar files
dataset = (
    wds.WebDataset("data/shard-{000000..000999}.tar")
    .shuffle(1000)
    .decode("pil")
    .to_tuple("jpg", "json")
    .map_tuple(transform_image, transform_label)
    .batched(32)
)

# Use with DataLoader
dataloader = wds.WebLoader(dataset, num_workers=4)
```

## Data Preprocessing

### Image Preprocessing

```python
from torchvision import transforms
from PIL import Image

# Standard ImageNet preprocessing
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.4, 0.4, 0.4, 0.1),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])
```

### Text Preprocessing

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

def preprocess_text(examples):
    """Tokenize text data."""
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=2048,
        padding="max_length",
        return_tensors="pt",
    )

# Apply to dataset
dataset = dataset.map(
    preprocess_text,
    batched=True,
    num_proc=4,
    remove_columns=["text"],
)
```

### Multimodal Preprocessing

```python
from transformers import AutoProcessor

processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

def preprocess_vlm(examples):
    """Process image-text pairs for VLM."""
    images = [Image.open(p).convert("RGB") for p in examples["image_path"]]
    texts = examples["text"]

    # Process with VLM processor
    inputs = processor(
        images=images,
        text=texts,
        padding=True,
        truncation=True,
        max_length=2048,
        return_tensors="pt",
    )

    return {
        "pixel_values": inputs.pixel_values,
        "input_ids": inputs.input_ids,
        "attention_mask": inputs.attention_mask,
    }
```

## Data Augmentation

### Image Augmentation with Albumentations

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

train_augment = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.8, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1),
    A.GaussNoise(var_limit=(10, 50), p=0.3),
    A.GaussianBlur(blur_limit=(3, 7), p=0.3),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

# Use in dataset
class AugmentedDataset(Dataset):
    def __getitem__(self, idx):
        image = np.array(Image.open(self.image_paths[idx]))
        augmented = self.augment(image=image)
        return augmented["image"]
```

### RandAugment

```python
from torchvision.transforms import RandAugment

transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    RandAugment(num_ops=2, magnitude=9),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
```

### MixUp and CutMix

```python
import torch

def mixup(x, y, alpha=0.2):
    """MixUp augmentation."""
    lam = np.random.beta(alpha, alpha)
    batch_size = x.size(0)
    index = torch.randperm(batch_size)

    mixed_x = lam * x + (1 - lam) * x[index]
    y_a, y_b = y, y[index]

    return mixed_x, y_a, y_b, lam

def cutmix(x, y, alpha=1.0):
    """CutMix augmentation."""
    lam = np.random.beta(alpha, alpha)
    batch_size = x.size(0)
    index = torch.randperm(batch_size)

    # Get bounding box
    W, H = x.size(2), x.size(3)
    cut_rat = np.sqrt(1. - lam)
    cut_w = int(W * cut_rat)
    cut_h = int(H * cut_rat)

    cx = np.random.randint(W)
    cy = np.random.randint(H)
    x1 = np.clip(cx - cut_w // 2, 0, W)
    x2 = np.clip(cx + cut_w // 2, 0, W)
    y1 = np.clip(cy - cut_h // 2, 0, H)
    y2 = np.clip(cy + cut_h // 2, 0, H)

    x[:, :, y1:y2, x1:x2] = x[index, :, y1:y2, x1:x2]
    lam = 1 - ((x2 - x1) * (y2 - y1) / (W * H))

    return x, y, y[index], lam
```

## Streaming and Sharding

### Streaming Large Datasets

```python
from datasets import load_dataset

# Stream without downloading entire dataset
dataset = load_dataset("HuggingFaceH4/ultrachat_200k", split="train", streaming=True)

# Iterate through stream
for example in dataset:
    # Process example
    pass

# Batch streaming
from torch.utils.data import IterableDataset

class StreamingDataset(IterableDataset):
    def __init__(self, dataset):
        self.dataset = dataset

    def __iter__(self):
        for example in self.dataset:
            yield self.process(example)
```

### Creating Sharded Datasets

```python
import webdataset as wds

def create_shards(data, output_pattern, samples_per_shard=10000):
    """Shard dataset into tar files."""
    with wds.ShardWriter(output_pattern, maxcount=samples_per_shard) as sink:
        for idx, item in enumerate(data):
            sample = {
                "__key__": f"{idx:08d}",
                "image.jpg": item["image"],
                "label.json": json.dumps(item["label"]),
            }
            sink.write(sample)

# Create shards
create_shards(dataset, "output/shard-%06d.tar")
```

### Distributed Data Loading

```python
from torch.utils.data.distributed import DistributedSampler

def create_distributed_loader(dataset, batch_size, rank, world_size):
    """Create DataLoader for distributed training."""
    sampler = DistributedSampler(
        dataset,
        num_replicas=world_size,
        rank=rank,
        shuffle=True,
    )

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=4,
        pin_memory=True,
    )

    return loader, sampler

# In training loop
for epoch in range(num_epochs):
    sampler.set_epoch(epoch)  # Important for shuffling
    for batch in loader:
        # Training step
        pass
```

## Data Quality

### Data Cleaning

```python
from datasets import Dataset

def clean_dataset(dataset):
    """Clean and filter dataset."""

    def is_valid(example):
        # Check for empty/missing fields
        if not example["text"] or len(example["text"]) < 10:
            return False
        # Check for duplicates (basic)
        # Check for quality issues
        return True

    # Filter invalid examples
    cleaned = dataset.filter(is_valid)

    # Remove duplicates
    cleaned = cleaned.map(lambda x: {"text_hash": hash(x["text"])})
    seen = set()
    def dedupe(example):
        if example["text_hash"] in seen:
            return False
        seen.add(example["text_hash"])
        return True
    cleaned = cleaned.filter(dedupe)

    return cleaned
```

### Data Validation

```python
from typing import Optional
from pydantic import BaseModel, validator

class DataSample(BaseModel):
    """Validate data sample schema."""
    image_path: str
    caption: str
    width: int
    height: int

    @validator("image_path")
    def check_image_exists(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Image not found: {v}")
        return v

    @validator("caption")
    def check_caption_length(cls, v):
        if len(v) < 5 or len(v) > 1000:
            raise ValueError("Caption length out of range")
        return v

def validate_dataset(data_path):
    """Validate entire dataset."""
    with open(data_path) as f:
        for i, line in enumerate(f):
            try:
                item = json.loads(line)
                DataSample(**item)
            except Exception as e:
                print(f"Invalid sample at line {i}: {e}")
```

## Memory-Efficient Processing

### Lazy Loading

```python
class LazyDataset(Dataset):
    """Load data on-demand to save memory."""

    def __init__(self, index_file: str):
        # Only load index, not data
        with open(index_file) as f:
            self.index = json.load(f)

    def __len__(self):
        return len(self.index)

    def __getitem__(self, idx):
        # Load actual data when needed
        path = self.index[idx]["path"]
        return self._load_item(path)

    def _load_item(self, path):
        # Load and process single item
        pass
```

### Memory-Mapped Files

```python
import numpy as np

# Create memory-mapped array
mmap = np.memmap("data.bin", dtype=np.float32, mode='w+', shape=(1000000, 768))

# Write data
for i, embedding in enumerate(embeddings):
    mmap[i] = embedding
mmap.flush()

# Read efficiently
mmap = np.memmap("data.bin", dtype=np.float32, mode='r', shape=(1000000, 768))
batch = mmap[100:200]  # Only loads requested slice
```

## Best Practices

1. **Use num_workers > 0** for DataLoader
2. **Enable pin_memory** for GPU training
3. **Precompute expensive transformations** when possible
4. **Use appropriate data formats** (WebDataset for large, HF datasets for medium)
5. **Validate data quality** before training
6. **Monitor data loading speed** with profiler
7. **Cache preprocessed data** for iterative development
8. **Use streaming** for datasets that don't fit in memory

# Imports
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType

# 1.Config
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # llama3.2:latest
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# 2 Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# 3 Load model
model = AutoModelForCausalLM.from_pretrained(
    model_name, quantization_config=bnb_config, device_map="auto"
)

# 4 Load LoRA config
lora_config = LoraConfig(
    r=8,  # Rank of the LoRA matrices, the higher the better. 8, 16, 32.
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, lora_config)

# 5 Load dataset
data = load_dataset("openai/gs8k", "main", split="train[:200]")


# 6 Tokenization function
def tokenize(batch):
    texts = [
        f"### Instruction:\n{inst}\n### Response:\n{out}"
        for inst, out in zip(batch["instruction"], batch["response"])
    ]

    tokens = tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=256,
        return_tensors="pt",
    )

    tokens["labels"] = tokens["input_ids"].clone()
    return tokens


# 7 Tokenize the dataset
tokenized_data = data.map(tokenize, batched=True, remove_columns=data.column_names)

# 8 Training arguments
training_args = TrainingArguments(
    output_dir="./lora-tinyllama",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    num_train_epochs=50,
    learning_rate=1e-3,
    fp16=True,
    logging_steps=20,
    save_strategy="epoch",
    remove_unused_columns=False,
    report_to="none",
)
# 9 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data,
    processing_class=tokenizer,
)

# 10 Train the model
trainer.train()

import torch
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Add a new padding token
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Load your Parquet dataset
dataset_path = "data/cleaned_dataset.parquet"
df = pd.read_parquet(dataset_path)

# Prepare training examples
training_examples = []

for index, row in df.iterrows():
    # Assuming 'input' column contains the input text
    input_text = row['input']
    
    # Add your custom instructions if needed
    instruction = "If you are a doctor, please answer the medical questions based on the patient's description."
    
    # Tokenize instruction and input text separately
    instruction_ids = tokenizer.encode(instruction, add_special_tokens=True)
    
    # Check if the combined length exceeds the model's maximum sequence length
    max_length = model.config.max_position_embeddings - len(instruction_ids)
    
    # Truncate or split input text to fit within the model's maximum sequence length
    input_ids = tokenizer.encode(input_text, add_special_tokens=True, max_length=max_length, truncation=True)
    
    # Combine instruction and input text
    combined_ids = instruction_ids + input_ids
    training_examples.append(combined_ids)

# Prepare data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # We are not doing masked language modeling
)

# Training arguments
training_args = TrainingArguments(
    output_dir="output",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

# Fine-tune the model
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=TextDataset(training_examples, tokenizer=tokenizer),
)

trainer.train()

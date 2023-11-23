from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can use "gpt2-medium", "gpt2-large", etc., for different sizes
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Example input text
input_text = "Hey you are a doctor, what advice would you give if i say i have a headache"

# Tokenize the input text
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate text using the model
output = model.generate(input_ids, max_length=300, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95)

# Decode the generated output
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# Print the generated text
print("Generated Text:")
print(generated_text)

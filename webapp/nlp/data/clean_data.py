import pandas as pd

# Load the Parquet dataset
dataset_path = "data/IOdata.parquet"
df = pd.read_parquet(dataset_path)

# Filter and remove rows with input length longer than 350 characters
df = df[df['input'].apply(lambda x: len(str(x)) <= 350)]

# Save the cleaned dataset back to Parquet
cleaned_dataset_path = "cleaned_IOdata.parquet"
df.to_parquet(cleaned_dataset_path, index=False)

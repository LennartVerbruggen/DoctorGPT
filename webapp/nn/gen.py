# Install necessary libraries
# pip install tensorflow pandas numpy

import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding
import pandas as pd
import numpy as np

# Load your dataset
# Replace 'your_dataset.csv' with the actual path to your dataset file
df = pd.read_parquet('data/data.parquet')

# Split the data into input (X) and output (y)
X = df['input'].values
y = df['output'].values

# Tokenize the text
tokenizer_X = Tokenizer(filters='')
tokenizer_X.fit_on_texts(X)
X_seq = tokenizer_X.texts_to_sequences(X)
X_pad = pad_sequences(X_seq, padding='post')

tokenizer_y = Tokenizer(filters='')
tokenizer_y.fit_on_texts(y)
y_seq = tokenizer_y.texts_to_sequences(y)
y_pad = pad_sequences(y_seq, padding='post')

# Define the model architecture
embedding_dim = 128
latent_dim = 256

# Encoder
encoder_inputs = Input(shape=(None,))
encoder_embedding = Embedding(input_dim=len(tokenizer_X.word_index) + 1, output_dim=embedding_dim)(encoder_inputs)
encoder_lstm = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(None,))
decoder_embedding = Embedding(input_dim=len(tokenizer_y.word_index) + 1, output_dim=embedding_dim)(decoder_inputs)
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = Dense(len(tokenizer_y.word_index) + 1, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Compile the model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
batch_size = 32
epochs = 10
model.fit([X_pad, y_pad[:, :-1]], np.expand_dims(y_pad[:, 1:], -1), batch_size=batch_size, epochs=epochs, validation_split=0.2)

# Save the tokenizer for later use
import pickle
with open('tokenizer_X.pickle', 'wb') as handle:
    pickle.dump(tokenizer_X, handle)

with open('tokenizer_y.pickle', 'wb') as handle:
    pickle.dump(tokenizer_y, handle)

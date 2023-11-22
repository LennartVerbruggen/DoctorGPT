from unittest.util import _MAX_LENGTH
import tensorflow as tf
import numpy as np
import pickle
from keras.preprocessing.sequence import pad_sequences

# Load the trained model
model = tf.keras.models.load_model('your_trained_model.h5')

# Load the tokenizers
with open('tokenizer_X.pickle', 'rb') as handle:
    tokenizer_X = pickle.load(handle)

with open('tokenizer_y.pickle', 'rb') as handle:
    tokenizer_y = pickle.load(handle)

# Function to generate a response
def generate_response(input_text):

    # Tokenize the input text
    input_seq = tokenizer_X.texts_to_sequences([input_text])
    input_pad = pad_sequences(input_seq, padding='post')

    # Initialize the decoder input with a start token
    decoder_input = np.zeros((1, 1))
    decoder_input[0, 0] = tokenizer_y.word_index['<start>']

    # Initialize the response
    response = ''

    while True:
        # Predict the next token
        predictions = model.predict([input_pad, decoder_input])
        predicted_token = np.argmax(predictions[0, -1, :])

        # Convert the predicted token to a word
        predicted_word = tokenizer_y.index_word[predicted_token]

        # Break the loop if the end token is predicted or the response reaches a maximum length
        if predicted_word == '<end>' or len(response.split()) > _MAX_LENGTH:
            break

        # Update the response
        response += ' ' + predicted_word

        # Update the decoder input for the next iteration
        decoder_input = np.zeros((1, 1))
        decoder_input[0, 0] = predicted_token

    return response.strip()

# Example usage
input_text = "User input text here."
response = generate_response(input_text)
print(f"Generated Response: {response}")

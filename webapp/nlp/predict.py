# predict.py

import pandas as pd
import joblib
import random
import json
import os

def predict_disease_and_precautions(user_input):
    # Get the absolute path of the current script
    script_path = os.path.abspath(__file__)

    # Construct the absolute path to 'symptom_model.joblib' based on the script's location
    model_path = os.path.join(os.path.dirname(script_path), 'symptom_model.joblib')

    # Load the trained model
    model = joblib.load(model_path)

    # Make predictions
    prediction = model.predict([user_input])

    # Retrieve precautions based on predicted disease
    precautions = get_precautions(prediction[0])

    # Generate a human-readable response
    response = generate_response(prediction[0], precautions)

    return response

def get_precautions(disease):
    # Get the absolute path of the current script
    script_path = os.path.abspath(__file__)

    # Construct the absolute path to 'data.csv' based on the script's location
    data_path = os.path.join(os.path.dirname(script_path), 'data/DSPdata.csv')

    # Load data
    data = pd.read_csv(data_path)

    # Find the row corresponding to the predicted disease
    row = data[data['disease'] == disease]

    # Extract precautions from the row
    precautions = row['precautions'].values[0] if not row.empty else "Precautions not available for this disease."

    return precautions

def generate_response(disease, precautions):
    # Get the absolute path of the current script
    script_path = os.path.abspath(__file__)

    # Construct the absolute path to 'templates.json' based on the script's location
    templates_path = os.path.join(os.path.dirname(script_path), 'templates.json')

    # Open the list of response templates
    with open(templates_path, 'r') as file:
        data = json.load(file)

    # Get the list of templates for the predicted disease
    templates = data["templates"]

    # Get a random template
    template = random.choice(templates)

    # Insert disease and precautions into the template
    response = template.format(disease, precautions)

    return response

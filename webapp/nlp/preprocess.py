import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data():
    # Load data
    data = pd.read_csv('data/DSPdata.csv')

    # Split data into features (X) and labels (y)
    X = data['symptoms']
    y = data['disease']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test




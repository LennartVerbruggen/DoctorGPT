import os.path
from preprocess import preprocess_data
from train import evaluate_model, train_model
from predict import predict_disease_and_precautions

def main():
    # Check if the model file exists
    if not os.path.exists('symptom_model.joblib'):
        print("Training the model...")
        X_train, X_test, y_train, y_test = preprocess_data()
        train_model(X_train, y_train)
        evaluate_model(X_test, y_test)
        print("Model created and trained successfully.")
    else:
        print("Model already exists.")


if __name__ == "__main__":
    main()

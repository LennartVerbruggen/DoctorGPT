import joblib
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import joblib

def train_model(X_train, y_train):
    # Create and train the model
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'symptom_model.joblib')

def evaluate_model(X_test, y_test):
    # Load the trained model
    model = joblib.load('symptom_model.joblib')

    # Evaluate the model on the test set
    accuracy = model.score(X_test, y_test)
    return accuracy * 100


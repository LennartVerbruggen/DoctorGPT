from src.data_loader import load_data
from src.feature_extraction import vectorize_text
from src.model import train_logistic_regression, load_trained_model, predict_disease
from src.evaluation import evaluate_model

# Load and preprocess data
train_data = load_data('data/train.jsonl')
test_data = load_data('data/test.jsonl')

X_train = [example['input_text'] for example in train_data]
y_train = [example['output_text'] for example in train_data]
X_test = [example['input_text'] for example in test_data]
y_test = [example['output_text'] for example in test_data]

# Vectorize text data
vectorizer, X_train_tfidf = vectorize_text(X_train, max_features=1000)
X_test_tfidf = vectorizer.transform(X_test)

# Train or load the Logistic Regression model
# If the model doesn't exist, train and save it
# Otherwise, load the pre-trained model
try:
    clf = load_trained_model('models/finalized_model.pkl')
except FileNotFoundError:
    clf = train_logistic_regression(X_train_tfidf, y_train, 'models/finalized_model.pkl')

# Make predictions on the test set
y_pred = clf.predict(X_test_tfidf)

# Evaluate the model
accuracy = evaluate_model(y_test, y_pred)

# Example usage
input_text = "My urine is black"
predicted_disease = predict_disease(input_text, vectorizer, clf)
print("Predicted Disease:", predicted_disease)

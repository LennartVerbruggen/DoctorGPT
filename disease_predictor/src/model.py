import pickle
from sklearn.linear_model import LogisticRegression

def train_logistic_regression(X_train_tfidf, y_train, model_filename='finalized_model.pkl'):
    clf = LogisticRegression()
    clf.fit(X_train_tfidf, y_train)
    
    # Save the trained model to disk
    with open(model_filename, 'wb') as model_file:
        pickle.dump(clf, model_file)

    return clf

def load_trained_model(model_filename='finalized_model.pkl'):
    with open(model_filename, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_disease(input_text, vectorizer, model):
    # Preprocess the input text
    input_tfidf = vectorizer.transform([input_text])

    # Make predictions
    prediction = model.predict(input_tfidf)

    return prediction[0]

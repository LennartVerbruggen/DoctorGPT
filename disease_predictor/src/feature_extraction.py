from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_text(text_data, max_features=1000):
    vectorizer = TfidfVectorizer(max_features=max_features)
    X_tfidf = vectorizer.fit_transform(text_data)
    return vectorizer, X_tfidf

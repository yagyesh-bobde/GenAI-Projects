import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from io import StringIO

# Sidebar - Allows user to upload a CSV file
st.sidebar.title('Upload CSV File')
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Placeholder for the DataFrame
df = None

# If a file is uploaded, load it into a DataFrame
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.dropna(inplace=True)
    df.drop(columns=["title", "author", "id"], inplace=True)
    df = df.iloc[:1500]

    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

    # Feature extraction using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    # Training a classifier (Random Forest in this example)
    classifier = RandomForestClassifier(n_estimators=100)
    classifier.fit(X_train_tfidf, y_train)

    # Main content
    st.title('Text Classification using RandomForest')

    # Display dataset
    st.write('Sample Dataset:')
    st.write(df.head())

    # Input text for prediction
    input_text = st.text_input("Enter text for prediction:", "")
    if input_text != "":
        X_new = tfidf_vectorizer.transform([input_text])
        prediction = classifier.predict(X_new)
        if prediction[0] == 1:
            st.write("Prediction: Genuine")
        else:
            st.write("Prediction: Fake")

    # Display model performance
    predictions = classifier.predict(X_test_tfidf)
    

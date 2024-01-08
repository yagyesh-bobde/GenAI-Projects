import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Example dataset (you'll need labeled data)
df=pd.read_csv("train.csv")
# to drop nan values
df.dropna(inplace=True)

#remove unnecessary columns
df.drop(columns=["title","author","id"],inplace=True)

df=df.iloc[:1500]


# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Feature extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Training a classifier (Random Forest in this example)
classifier = RandomForestClassifier(n_estimators=100)
classifier.fit(X_train_tfidf, y_train)

# Predicting on the test set
predictions = classifier.predict(X_test_tfidf)

# Evaluating performance
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")
print("\n")


report = classification_report(y_test, predictions)
print(f"Classification Report:\n{report}")
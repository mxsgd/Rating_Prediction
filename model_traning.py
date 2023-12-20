import csv
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import joblib

with open('data.csv', 'r', encoding='utf-8', newline='') as csvfile:
    content = list(csv.reader(csvfile))

nlp = spacy.load("en_core_web_md")

reviews = []
ratings = []

for review in content:
    review_text = re.sub(r'<[^>]+>|\\n|\.|,|:|&|;|-|"|!|@|#|\$|%|\^|\*|\(|\)|\[|\]|\{|\}|\?|\’', '', review[0])
    tok = nlp(review_text)
    review_proc = ' '.join([token.text for token in tok if not token.is_stop])
    reviews.append(review_proc)
    ratings.append(int(review[1]))

y = [[rating] for rating in ratings]
tfidf_vectorizer = TfidfVectorizer()

X_tfidf = tfidf_vectorizer.fit_transform(reviews)


X_train, X_test, y_train, y_test = train_test_split(X_tfidf,y,
                                                    test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

joblib.dump(model, 'review_prediction_model.joblib')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
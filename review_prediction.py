import joblib
import re
import spacy

model = joblib.load('review_prediction_model.joblib')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')
with open('review_to_predict.txt', encoding='utf-8') as f:
    review_text = f.read()

nlp = spacy.load("en_core_web_sm")

review_text = re.sub(r'<[^>]+>|\\n|\.|,|:|&|;|-|"|!|@|#|\$|%|\^|\*|\(|\)|\[|\]|\{|\}|\?|\’', '', review_text)

tok = nlp(review_text)
review_proc = ' '.join([token.text for token in tok if not token.is_stop])

X_tfidf = tfidf_vectorizer.transform([review_proc])

print(model.predict(X_tfidf))
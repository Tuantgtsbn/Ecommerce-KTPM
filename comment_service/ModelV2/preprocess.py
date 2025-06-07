import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
def preprocess(test_features):
    processed_test_features = []

    for sentence in range(0, len(test_features)):
    
    # Remove all special characters
        processed_feature = re.sub(r'\W', ' ', str(test_features[sentence]))
    
    # Remove all words that include digits / numbers
        processed_feature = re.sub(r'\w*\d\w*', ' ', processed_feature)
    
    # Remove all single characters
        processed_feature = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)
    
    # Remove single characters from the start
        processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)
    
    # Substituing multiple spaces with single space
        processed_feature = re.sub(r'\s+', ' ', processed_feature, flags = re.I)
    
    # Converting to lowercase
        processed_featured = processed_feature.lower()
    
    # Append cleaned review to processed list
        processed_test_features.append(processed_feature)
    vectorizer = TfidfVectorizer(max_features = 2500, min_df = 1, max_df = 0.9, stop_words = stopwords.words('english'))
    processed_test_features = vectorizer.fit_transform(processed_test_features).toarray()
    return processed_test_features

def load_model(path_name: str):
    return joblib.load(path_name)

test_raw = pd.read_csv(r'comment_service\ClassifyCommentModel\input\test.csv')
test_sub = test_raw.iloc[:1000].copy()
test_features = test_sub.iloc[:,1].values
processed_test_features = preprocess(test_features)
model = load_model(r'comment_service\ClassifyCommentModel\rfc_model_02.pkl')
predictions = model.predict(processed_test_features)
test_sub['label'] = predictions
test_sub.to_csv(r'comment_service\ClassifyCommentModel\test_sub.csv', index=False)

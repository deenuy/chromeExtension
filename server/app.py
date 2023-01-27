from nltk.tokenize import TweetTokenizer   # module for tokenizing strings
from nltk.stem import WordNetLemmatizer    # module for lemmatization
from nltk.stem.porter import PorterStemmer  # module for stemming
# module for stop words that come with NLTK
from nltk.corpus import stopwords
import re
import numpy as np
from flask import Flask, request, jsonify, render_template, Response, render_template_string
import pickle
import sys
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score, classification_report, f1_score, roc_curve
from sklearn.metrics import classification_report
import string
import nltk
import skmultilearn
import json
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import GaussianNB

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# download the stopwords from NLTK
PUNCT_TO_REMOVE = string.punctuation
STOPWORDS = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def text_preprocessing(text):
    # Lowercasing
    text = text.lower()

    # Stopword Removal
    STOPWORDS = set(stopwords.words('english'))
    text = " ".join([word for word in str(
        text).split() if word not in STOPWORDS])

    # Punctuation Removal
    text = text.translate(str.maketrans('', '', string.punctuation))

    # url Removal
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = url_pattern.sub(r'', text)

    # Noise Removal
    text = re.sub("(<.*?>)", "", text)
    text = re.sub("(\\W|\\d)", " ", text)
    text = text.strip()
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Stemming or lemmatization
    lemmatizer = WordNetLemmatizer()
    # stemmer = SnowballStemmer("english")
    # text = [stemmer.stem(word) for word in text.split()]
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    return text


# Create flask app
flask_app = Flask(__name__, template_folder='templates',
                  static_folder='static')

flask_app.config.from_pyfile('config.py')

# Import ml model
RQ1_model = pickle.load(open("ml-model/RQ1_trained_model.pkl", "rb"))
# RQ2_model = pickle.load(open("ml-model/RQ2_trained_model.pkl", "rb"))
# Importing a saved model occurs error in data consistency
# As an alternative, we can train new model when the server starts


@flask_app.route('/')
def product():
    return render_template('index.html')

# Prediction API - POST method


@flask_app.route("/imager_predict", methods=["POST"])
def predict():
    # Bugzilla form data from API request
    form_data = request.get_json()

    # Console log
    print("\n*************************")
    print(form_data)
    print("\n*************************\n")

    # Get the summary from the form data
    summary = form_data['summary']
    print('INFO: line 104: ', summary)

    # preprocess the summary
    summary = text_preprocessing(summary)
    print('INFO: line 108: ', summary)

    # Convert the summary string to numpy array
    summary = np.array([f'{summary}'])
    print('INFO: line 111: ', summary)
    print('INFO: line 111: Type - ', type(summary))
    print('INFO: line 111: Shape - ', summary.shape)

    # RQ1 predication - Whether or not should the user include the image?
    try:
        RQ1_predication = RQ1_model.predict(summary)
        print('INFO: line 123; RQ1 Prediction Result: ', RQ1_predication)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f'\nERROR: RQ1 Prediction failed at line {exc_tb.tb_lineno}')
        print(exc_type, fname, exc_tb.tb_lineno, '\n')

    # RQ2 predication - Which type of image should the user include?

    RQ2_predication_dict = {}

    # If needed, run RQ2_model to predict the probability of each image type
    if RQ1_predication == 1:
        # Read train data from csv
        train = pd.read_csv('train_data.csv')

        # Read test data from user input (has been preprocessed in RQ1)
        test = summary

        # Vectorize the train & test data
        vectorizer = TfidfVectorizer(
            strip_accents='unicode', analyzer='word', ngram_range=(1, 3), norm='l2')
        vectorizer.fit(train.summary)
        vectorizer.fit(test)

        X_train = vectorizer.transform(train.summary)
        test = vectorizer.transform(test)
        train = train.drop('Unnamed: 0', axis=1)
        y_train = train.drop(labels=['img_name', 'labels', 'severity', 'op_sys', 'component',
                                     'keywords', 'summary', 'platform', 'product', 'priority', 'type', 'status'], axis=1)

        classifier = BinaryRelevance(GaussianNB())
        # train
        classifier.fit(X_train, y_train)
        # predict with probabilities
        RQ2_predication_tmp = classifier.predict_proba(test)

        # Convert the prediction result to dictionary
        RQ2_predication_tmp = RQ2_predication_tmp.toarray()
        RQ2_predication_tmp = RQ2_predication_tmp.tolist()

        # the 4th is none of the above, so we don't need it
        RQ2_predication_dict['Code'] = round(
            RQ2_predication_tmp[0][0] * 100, 3)
        RQ2_predication_dict['Run Time Error'] = round(
            RQ2_predication_tmp[0][1] * 100, 3)
        RQ2_predication_dict['Menus and Preferences'] = round(
            RQ2_predication_tmp[0][2] * 100, 3)
        # RQ2_predication_dict['None'] = RQ2_predication_tmp[0][3]
        RQ2_predication_dict['Program Input'] = round(
            RQ2_predication_tmp[0][4] * 100, 3)
        RQ2_predication_dict['Desired Output'] = round(
            RQ2_predication_tmp[0][5] * 100, 3)
        RQ2_predication_dict['Program Output'] = round(
            RQ2_predication_tmp[0][6] * 100, 3)
        RQ2_predication_dict['Dialog Box'] = round(
            RQ2_predication_tmp[0][7] * 100, 3)
        RQ2_predication_dict['Steps and Processes'] = round(
            RQ2_predication_tmp[0][8] * 100, 3)
        RQ2_predication_dict['CPU/GPU Performance'] = round(
            RQ2_predication_tmp[0][9] * 100, 3)
        RQ2_predication_dict['Algorithm/Concept Description'] = round(
            RQ2_predication_tmp[0][10] * 100, 3)

        print('\n\nINFO: line 162; RQ2 Prediction Result: ')
        print(RQ2_predication_dict)

    else:
        RQ2_predication_dict = {"message": "No image needed"}
        print(RQ2_predication_dict)

    data = json.dumps(RQ2_predication_dict)

    # Return RQ2 response to API
    return Response(data, status='HTTP_200_OK')


if __name__ == "__main__":
    # flask_app.run(debug=True)
    flask_app.run(host=flask_app.config['HOST'],
                  port=flask_app.config['PORT'], debug=flask_app.config['DEBUG'])

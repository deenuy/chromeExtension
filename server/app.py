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
import json
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
RQ2_model = pickle.load(open("ml-model/RQ2_trained_model.pkl", "rb"))

# Welcome page at root


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

    # RQ1_predication = []
    # RQ2_predication = {}

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
    # If needed, run RQ2_model to predict the probability of each image type
    # if RQ1_predication == 1:
    #     RQ2_predication = RQ2_model.predict_proba(summary)
    #     print(RQ2_predication)
    # else:
    #     RQ2_predication = {"message": "No image needed"}
    #     print(RQ2_predication)

    # data = json.dumps(RQ2_predication)

        # dummy data
        # prediction = model.predict(features)

    data2 = {
        "Code": 0.98,
        "Run Time Error": 0.71,
        "Menus and Preferences": 0.22,
        "Program Input": 0.21,
        "Desired Output": 0.11,
        "Program Output": 0.18,
        "Dialog Box": 0.52,
        "Steps and Processes": 0.75,
        "CPU/GPU Performance": 0.18,
        "Algorithm/Concept Description": 0.13
    }
    data2 = {
        "message": "no image needed"
    }

    data2 = json.dumps(data2)

    # Return RQ2 response to API
    return Response(data2, status='HTTP_200_OK')


if __name__ == "__main__":
    flask_app.run(debug=True)
    # app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

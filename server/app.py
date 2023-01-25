import numpy as np
from flask import Flask, request, jsonify, render_template, Response, render_template_string
import pickle

# Create flask app
# flask_app = Flask(__name__)

flask_app = Flask(__name__, template_folder='templates', static_folder='static')

flask_app.config.from_pyfile('config.py')
RQ1_model = pickle.load(open("ml-model/RQ1_trained_model.pkl", "rb"))
RQ2_model = pickle.load(open("ml-model/RQ2_trained_model.pkl", "rb"))

# Welcome page at root
@flask_app.route('/')
def product():
  return render_template('index.html')

# Prediction API - POST method (OBSOLETE- DO NOT USE IT)
@flask_app.route("/imager_predict/v1", methods = ["POST"])
def predict():
  float_features = [float(x) for x in request.form.values()]
  features = [np.array(float_features)]
  # prediction = RQ1_model.predict(features)
  
  # RQ1 predication - Whether or not should the user include the image?
  RQ1_predication = RQ1_model.predict(features)

  # RQ2 predication - Which type of image should the user include?
  # If needed, run RQ2_model to predict the probability of each image type
  if RQ1_predication == 1:
      RQ2_predication = RQ2_model.predict_proba(features)

  return render_template("index.html", prediction_text = "The probas of image type are {}".format(RQ2_predication))


# Prediction API - POST method
@flask_app.route("/imager_predict", methods = ["POST"])
def predict():
  # Bugzilla form data from API request
  form_data = request.get_json()
  
  # Console log
  print("\n*************************")
  print(form_data)
  print("\n*************************")
  
  ###########################################################
  #   Hi Tan! Insert your code here. Your input is form_data
  #   variable (received from API request). You will have to
  #   parse dictionary data and execute RQ1, RQ2, and generate 
  #   response as shown in line number 57. 
  
  #   INSERT YOUR CODE here
  ###########################################################

  # RQ2 response - dummy data
  rq2_result = {
    "Code" : 0.98,
    "Run Time Error" : 0.71, 
    "Menus and Preferences" : 0.22, 
    "Program Input" : 0.21, 
    "Desired Output" : 0.11, 
    "Program Output" : 0.18, 
    "Dialog Box" : 0.52, 
    "Steps and Processes" : 0.75, 
    "CPU/GPU Performance" : 0.18, 
    "Algorithm/Concept Description" : 0.13
  }
  data = json.dumps(rq2_result)
  
  # Return RQ2 response to API
  return Response(data, status='HTTP_200_OK')

if __name__ == "__main__":
  flask_app.run(debug=True)
  # app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
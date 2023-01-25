import numpy as np
from flask import Flask, request, jsonify, render_template, Response, render_template_string
import pickle, json

# Create flask app
# flask_app = Flask(__name__)

flask_app = Flask(__name__, template_folder='templates', static_folder='static')
 
flask_app.config.from_pyfile('config.py')
model = pickle.load(open("model.pkl", "rb"))

@flask_app.route('/')
def product():
  return render_template('index.html')

@flask_app.route("/imager_predict", methods = ["POST"])
def predict():
  data = request.get_json()
  
  print("\n\n")
  print(data)
  print("\n\n")

  # prediction = model.predict(features)
  data = {
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
  data = json.dumps(data)
  return Response(data, status='HTTP_200_OK')


if __name__ == "__main__":
  flask_app.run(debug=True)
  # app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
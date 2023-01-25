import numpy as np
from flask import Flask, request, jsonify, render_template, Response, render_template_string
import pickle

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
  return Response('Prediction API response is successful', status='HTTP_200_OK')

if __name__ == "__main__":
  flask_app.run(debug=True)
  # app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
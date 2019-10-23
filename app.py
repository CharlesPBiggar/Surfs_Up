#Flask App for Hawaii Weather Data

#!! Steps to run file (Git-Windows): 1) python app.py 2) python -m flask run

#import dependencies
from flask import Flask

app = Flask(__name__)

#create route, hello world
@app.route('/')
def hello_world():
    return 'Hello, World!'
from flask import Flask

app = Flask(__name__)

@app.route('lol')
def hello_world():
    return 'Hello, World!'
  

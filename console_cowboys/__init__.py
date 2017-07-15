from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app     = Flask(__name__)
app.config.from_object("console_cowboys.config")
db      = SQLAlchemy(app)

@app.route("/")
def index():
    return "Hello World"

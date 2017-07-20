from flask import Flask, request
from flask_cors  import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from .helpers import ErrorResponse

app     = Flask(__name__)
cors    = CORS(app)
app.config.from_object("console_cowboys.config")
app.config["CORS_HEADERS"] = 'Content-Type'
db      = SQLAlchemy(app)

from .models import Job

@app.route("/jobs")
@cross_origin()
def index():

    query_string = request.args.get("remote")

    if query_string and query_string.lower() == "true":
        return Job.remote()

    return Job.all()

@app.route("/jobs/<string:contract_type>")
def get_jobs_by_contract_type(contract_type):
    return Job.filter_by_contract_type(contract_type)


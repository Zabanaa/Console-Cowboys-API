import stripe
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from .helpers import Response, ErrorResponse

app     = Flask(__name__)
app.config.from_object("console_cowboys.config")
db      = SQLAlchemy(app)

# Setup stripe keys
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

from .models import Job
from .decorators import protected, crossdomain

cors = CORS(app, resources={r'/*': {"origins": "*"}})

@app.route("/jobs")
def index():

    query_string = request.args.get("remote")

    if query_string and query_string.lower() == "true":
        return Job.remote()

    return Job.all()

@app.route("/jobs/<string:contract_type>")
def get_jobs_by_contract_type(contract_type):
    return Job.filter_by_contract_type(contract_type)

@app.route("/jobs/checkout", methods=["POST"])
@cross_origin(origin="*")
@protected
def publish_job():

    job_data        = request.get_json()

    job_data        = json.loads(job_data)

    customer = stripe.Customer.create(
        source=job_data["stripe_token"]
    )

    try:
        charge = stripe.Charge.create(
            amount=7900,
            currency="usd",
            customer=customer.id,
            description="{} @ {}".format(job_data["job_title"],job_data["company_name"])
        )
    except Exception as e:
        print("Something bad happened: ", e)

    else:
        job_data["charge_id"]   = charge.id
        job_data["is_paid"]     = True

    return Job.create(job_data)

@app.route("/jobs/publish", methods=["POST"])
def publish_automated_job():
    body = request.get_json()
    return Job.create(body)

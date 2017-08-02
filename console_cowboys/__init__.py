import stripe
from flask import Flask, request
from flask_cors  import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from .helpers import Response, ErrorResponse

app     = Flask(__name__)
app.config.from_object("console_cowboys.config")
app.config["CORS_HEADERS"] = 'Content-Type'
db      = SQLAlchemy(app)

cors    = CORS(app, resources={r"/jobs/*": { "origins": "*" }})

# Setup stripe keys
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

from .models import Job
from .decorators import protected

@app.route("/jobs")
@cross_origin(origin="*", headers=["Content-Type"])
def index():

    query_string = request.args.get("remote")

    if query_string and query_string.lower() == "true":
        return Job.remote()

    return Job.all()

@app.route("/jobs/<string:contract_type>")
@cross_origin(origin="*", headers=["Content-Type"])
def get_jobs_by_contract_type(contract_type):
    return Job.filter_by_contract_type(contract_type)

@app.route("/jobs/checkout", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def publish_job():

    if request.headers["Content-Type"] == "application/json":
        return ErrorResponse.json_invalid()

    job_data = {
        "listing_url": request.form["listing_url"],
        "is_remote": request.form["is_remote"],
        "company_name": request.form["company_name"],
        "title": request.form["job_title"],
        "contract_type": request.form["contract_type"],
        "location": request.form["location"],
    }

    customer = stripe.Customer.create(
        source=request.form["stripe_token"]
    )

    try:
        charge = stripe.Charge.create(
            amount=7900,
            currency="usd",
            customer=customer.id,
            description="{} @ {}".format(job_data["title"],job_data["company_name"])
        )
    except Exception as e:
        print("Something Happened", e)

    job_data["charge_id"]   = charge.id
    job_data["is_paid"]     = True

    return Job.create(job_data)


@app.route("/jobs/publish", methods=["POST"])
def publish_automated_job():
    body = request.get_json()
    return Job.create(body)

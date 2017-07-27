import stripe
from flask import Flask, request
from flask_cors  import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from .helpers import Response, ErrorResponse

app     = Flask(__name__)
cors    = CORS(app)
app.config.from_object("console_cowboys.config")
app.config["CORS_HEADERS"] = 'Content-Type'
db      = SQLAlchemy(app)

# Setup stripe keys
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

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

@app.route("/jobs/checkout", methods=["POST"])
@cross_origin()
def publish_job():

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
            description="{} @ {}".format(job_data["title"],job_data["location"])
        )
    except Exception as e:
        print("Something Happened", e)

    job_data["charge_id"]   = charge.id
    job_data["is_paid"]     = True

    Job.create(job_data)

    return Response.created()

    # Step 2: if it's a json request
    # check that there's a token then verify the token
    # if they don't match return a 401

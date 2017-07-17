from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app     = Flask(__name__)
app.config.from_object("console_cowboys.config")
db      = SQLAlchemy(app)

from .models import Job

@app.route("/api/jobs")
def index():
    return Job.all()

@app.route("/api/jobs/full-time")
def get_full_time_jobs():
    return Job.filter_by_contract_type("full-time")

@app.route("/api/jobs/freelance")
def get_freelance_jobs():
    return Job.filter_by_contract_type("freelance")

@app.route("/api/jobs/internship")
def get_internship_jobs():
    return Job.filter_by_contract_type("internship")



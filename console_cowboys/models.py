from datetime import datetime
from console_cowboys.helpers import Response, ErrorResponse
from console_cowboys import db
from sqlalchemy_utils import ChoiceType
from sqlalchemy.exc import IntegrityError

class Job(db.Model):

    CONTRACT_TYPES = [
        ("full-time", "Full Time"),
        ("freelance", "Freelance / Contract"),
        ("internship", "Internship")
    ]

    id                  = db.Column(db.Integer, primary_key=True)
    title               = db.Column(db.String(90), nullable=False)
    location            = db.Column(db.String(90), nullable=False)
    contract_type       = db.Column(ChoiceType(CONTRACT_TYPES), nullable=False)
    company_name        = db.Column(db.String(90), nullable=False)
    listing_url         = db.Column(db.String(90), nullable=False, unique=True)
    is_remote           = db.Column(db.Boolean, default=False)
    is_paid             = db.Column(db.Boolean, default=False)
    date_added          = db.Column(db.DateTime, default=datetime.utcnow)
    charge_id           = db.Column(db.String(70))

    def __init__(self, json_payload):

        for key, value in json_payload.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, payload):
        """
            Creates a new Job object, passing it the json_payload
            from the request.
            Immediately call .save() on it

        """
        return cls(payload).save()

    def save(self):

        """
            Saves the instance to the DB
        """

        try:
            db.session.add(self)
            db.session.commit()

        except IntegrityError as e:

            cause_of_error = str(e.__dict__["orig"])

            if "not-null" in cause_of_error:
                missing_fields = e.__dict__["params"]
                return ErrorResponse.missing_fields_error(missing_fields)

            elif "unique" in cause_of_error:
                return ErrorResponse.unique_field_error(cause_of_error)

            else:
                print(e) # Eventually log it
                return ErrorResponse.server_error()

        return self


    def to_dict(self):

        return {

            "title": self.title,
            "location": self.location,
            "contract_type": self.contract_type,
            "company_name": self.company_name,
            "listing_url": self.listing_url,
            "is_remote": self.is_remote,
        }

    @classmethod
    def all(cls):

        job_objects = cls.query.all()
        json_jobs   = [job.to_dict() for job in job_objects]

        try:
            return Response.ok(json_jobs)
        except Exception as e:
            # Log exception
            return ErrorResponse.server_error()

    @classmethod
    def filter_by_contract_type(cls, contract_type):

        job_objects = cls.query.filter_by(contract_type=contract_type).all()
        json_jobs   = [job.to_dict() for job in job_objects]

        return Response.ok(json_jobs)

    def __repr__(self):
        return "{} at {} in {}".format(self.title,
                                       self.company_name,
                                       self.location)


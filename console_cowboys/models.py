from datetime import datetime
from console_cowboys.helpers import ErrorResponse
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
                print(ErrorResponse.unique_field_error(cause_of_error))

            else:
                print("Something Happened")

        return self

    def __repr__(self):
        return "{} at {} in {}".format(self.title,
                                       self.company_name,
                                       self.location)


import re
from flask import jsonify

class Response(object):

    @classmethod
    def created(cls):

        body    = {
            "meta": {
                "type": "success",
                "status_code": 201
            },

            "body": {
                "message": "Job was sucessfully created"
            }

        }

        response                = jsonify(body)
        response.status_code    = 201
        response.headers["Server"] = "Don't worry bout it"

        return response

    @classmethod
    def ok(cls, jobs):

        body        = {
            "meta": {
                "type": "success",
                "status_code": 200
            },
            "body": {
                "count": len(jobs),
                "jobs": jobs
            }
        }
        response                = jsonify(body)
        response.status_code    = 200
        response.headers["Server"] = "Don't worry bout it"

        return response

class ErrorResponse(object):

    bad_request_msg = "You sent a request that our server could not understand. \
Please make sure it's properly formatted before resending."

    @classmethod
    def forbidden(cls):

        body = {
            "meta": {
                "type": "error",
                "status": 403
            },

            "body": {
                "message": "You are forbidden from posting to this endpoint"
            }
        }

        response = jsonify(body)
        response.status_code = 403
        response.headers["Server"] = "Don't Worry bout it"
        return response

    @classmethod
    def json_invalid(cls):

        body = {

            "meta": {
                "type": "error",
                "status": 400
            },
            "body": {
                "message": "This endpoint does not process json requests"
            }

        }

        response = jsonify(body)
        response.status_code = 400
        response.headers["Server"] = "Don't worry bout it"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @classmethod
    def get_missing_fields(cls, fields):

        missing_fields = []

        for key, value in fields.items():

            if key == "charge_id":
                continue

            if fields[key] is None:
                missing_fields.append(key)

        return missing_fields

    @classmethod
    def get_duplicate_key(cls, error_message):
        pattern         = re.compile("\(([^\)]+)\)")
        duplicate_key   = pattern.findall(error_message)[0]

        return duplicate_key

    @classmethod
    def unique_field_error(cls, error_message):

        duplicate_key   = cls.get_duplicate_key(error_message)

        response        = jsonify({

            "meta": {
                "type": "error",
                "status_code": 409
            },

            "body": {

                "message": "Missing fields",
                "fields": duplicate_key
            }

        })

        response.status_code = 409
        response.headers["Server"] = "Don't worry bout it"

        return response

    @classmethod
    def missing_fields_error(cls, missing_fields):

        missing_fields  = cls.get_missing_fields(missing_fields)

        response        =  jsonify({

            "meta": {
                "type": "error",
                "status_code": 422
            },

            "body": {

                "message": "Missing fields",
                "missing_fields": missing_fields
            }
        })

        response.status_code = 422
        response.headers["Server"] = "Don't worry bout it"

        return response


    @classmethod
    def server_error(cls):

        msg = "Something happened on our part. Please Hang tight while we fix the issue"

        response = jsonify({

            "meta": {
                "type": "error",
                "status_code": 500
            },

            "body": {

                "message": msg
            }
        })

        response.status_code = 500
        response.headers["Server"] = "Don't worry bout it"

        return response

    @classmethod
    def nonexistent_endpoint(cls):

        response    = jsonify({

            "meta": {
                "type": "error",
                "status_code": 404
            },

            "body": {

                "message": "The endpoint you're trying to reach does not exist."
            }
        })

        response.status_code = 404
        response.headers["Server"] = "Don't worry bout it"

        return response

    @classmethod
    def bad_request(cls, msg=bad_request_msg):

        response    = jsonify({

            "meta": {
                "type": "error",
                "status_code": 400
            },

            "body": {

                "message": msg
            }
        })

        response.status_code = 400
        response.headers["Server"] = "Don't worry bout it"

        return response


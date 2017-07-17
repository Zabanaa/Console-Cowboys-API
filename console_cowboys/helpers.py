import re
from flask import jsonify

class Response(object):

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
        return response

class ErrorResponse(object):

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

        duplicate_key = cls.get_duplicate_key(error_message)

        return jsonify({

            "meta": {
                "type": "error",
                "status_code": 409
            },

            "body": {

                "message": "Missing fields",
                "fields": duplicate_key
            }

        })

    @classmethod
    def missing_fields_error(cls, missing_fields):

        missing_fields = cls.get_missing_fields(missing_fields)

        return jsonify({

            "meta": {
                "type": "error",
                "status_code": 422
            },

            "body": {

                "message": "Missing fields",
                "missing_fields": missing_fields
            }
        })


    @classmethod
    def server_error(cls):

        msg = "Something happened on our part. Please Hang tight while we fix the issue"

        return jsonify({

            "meta": {
                "type": "error",
                "status_code": 500
            },

            "body": {

                "message": msg
            }
        })











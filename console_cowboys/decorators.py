from console_cowboys import app
from console_cowboys.helpers import ErrorResponse
from flask import request

def protected(func):

    def wrapped(*args, **kwargs):

        content_type = request.headers["Content-Type"]
        secret_key   = request.headers.get("X-Secret-Key")

        print(secret_key, app.config["SECRET_KEY"])

        if content_type != "application/json":

            return ErrorResponse.forbidden()

        else:

            if secret_key != app.config["SECRET_KEY"]:

                return ErrorResponse.forbidden()

        return func(*args, **kwargs)

    return wrapped

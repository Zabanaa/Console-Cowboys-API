import os

DEBUG       = os.getenv("CONSOLE_COWBOYS_DEBUG", True)
PORT        = os.getenv("CONSOLE_COWBOYS_PORT", 8081)
SECRET_KEY  = os.getenv("CONSOLE_COWBOYS_SECRET_KEY")

DB_USER     = os.getenv("CONSOLE_COWBOYS_DB_USER")
DB_HOST     = os.getenv("CONSOLE_COWBOYS_DB_HOST")
DB_PORT     = os.getenv("CONSOLE_COWBOYS_DB_PORT")
DB_NAME     = os.getenv("CONSOLE_COWBOYS_DB_NAME")
DB_PASS     = os.getenv("CONSOLE_COWBOYS_DB_PASSWORD")

STRIPE_SECRET_KEY = os.getenv("CONSOLE_COWBOYS_STRIPE_SECRET")
STRIPE_PUBLIC_KEY = os.getenv("CONSOLE_COWBOYS_STRIPE_PUBLIC")


SQLALCHEMY_DATABASE_URI    = "postgres://{}:{}@{}:{}/{}".format(
                                DB_USER,
                                DB_PASS,
                                DB_HOST,
                                DB_PORT,
                                DB_NAME
                            )

SQLALCHEMY_TRACK_MODIFICATIONS = False

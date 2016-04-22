import os

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/montenegro"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(20)

PAGE_LIMIT = 10

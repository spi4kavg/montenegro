import os
import hashlib
from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from app.views.auth import auth
from app.views.users import users
from app.views.api import api

app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(api)



@app.context_processor
def csrf():
    session['csrf'] = hashlib.sha1(os.urandom(64)).hexdigest()
    return dict(token=session['csrf'])

from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import check_password_hash, generate_password_hash
from app import db


class User(db.Model):
    ''' user model '''

    __tablename__ = 'auth_user'

    pk = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    grant = db.Column(db.Boolean())
    uuid = db.Column(db.String(128), nullable=True, index=True)

    def __init__(self, login, password, grant):
        self.login = login
        self.grant = grant
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % (self.login,)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)

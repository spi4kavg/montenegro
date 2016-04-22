# -*- coding: utf-8 -*-
from functools import wraps
from flask import request, session, redirect, url_for, abort, g
from models import User


def login_required(fn):
    ''' login required decorator '''
    def unauthorized():
        if request.is_xhr:
            abort(401)
        else:
            return redirect(url_for("auth.login"))

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "uuid" not in session:
            return unauthorized()
        else:
            user = User.query.filter_by(uuid=session['uuid']).first()
            if not user:
                return unauthorized()
            g.user = user
        return fn(*args, **kwargs)
    return wrapper


def xhr(fn):
    ''' is ajax decorator '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not request.is_xhr:
            abort(400)
        return fn(*args, **kwargs)
    return wrapper


def grant_required(fn):
    ''' checks user grants '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not g.user.grant:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


def csrf_protect(fn):
    ''' checks csrf protection '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE']:
            if request.is_xhr:
                token = request.headers.get('X-CSRFToken')
            else:
                token = request.form.get('csrftoken')
            if session.get("csrf") != token or token is None:
                abort(403)
        return fn(*args, **kwargs)
    return wrapper


class Validator(object):
    ''' simple validator for fields '''

    def __init__(self, form_data, validators):
        self.form_data = form_data
        self.validators = validators
        self.errors = {}
        for key in self.form_data:
            self.errors[key] = []

    def is_valid(self):
        valid = True
        for key, value in self.form_data.items():
            for validator in self.validators.get(key, []):
                method, args = self._get_validator(validator)
                if not method:
                    raise Exception("Validator {} not exist".format(
                        str(validator)
                    ))
                is_valid, message = method(value, *args)
                if not is_valid:
                    self.errors[key].append(message)
                    valid = is_valid
        return valid

    def is_equal(self, value, asigned_field):
        if not value == self.form_data[asigned_field]:
            return False, u"Значения полей не совпадают"
        return True, ""

    def min_length(self, value, str_len):
        if not len(value) >= int(str_len):
            return False, u"""
                Длина поля не должна быть меньше {} символов
            """.format(str_len)

        return True, ""

    def max_length(self, value, str_len):
        if not len(value) <= int(str_len):
            return False, u"""
                Длина поля не должна превышать {} символов
            """.format(str_len)
        return True, ""

    def is_string(self, value):
        if not isinstance(value, unicode):
            return False, u"Введен неверный формат поля"
        return True, ""

    def is_bool(self, value):
        bool_values = ['false', 'False', 'True', 'true', '1', '0']
        if isinstance(value, unicode):
            if value in bool_values:
                return True, ""
        elif isinstance(value, int):
            if value in [1, 0]:
                return True, ""
        elif isinstance(value, bool):
            return True, ""
        return False, u"Введен неверный формат поля"

    def empty(self, value):
        if not value:
            return False, u"Поле не может быть пустым"
        return True, ""

    def _get_validator(self, validator):
        method, args = "", ""
        if validator.find("|") >= 0:
            method, args = validator.split("|")
        else:
            method, args = validator, ""
        return getattr(self, method, None), args.split(",") if args else args

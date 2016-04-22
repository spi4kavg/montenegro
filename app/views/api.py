# -*- coding: utf-8 -*-
import re
from flask import Blueprint, request, jsonify, abort
from werkzeug import check_password_hash, generate_password_hash
from app import db
from app.config import PAGE_LIMIT
from app.models import User
from app import utils

api = Blueprint('api', __name__, url_prefix="/api")


@api.route('/list', methods=['GET'])
@utils.login_required
@utils.xhr
@utils.csrf_protect
def list():
    ''' gets user list '''
    page = request.args.get('page', 1)
    try:
        page = int(page) if int(page) >= 1 else 1
    except ValueError:
        page = 1
    users = User.query.paginate(page=page, per_page=PAGE_LIMIT)
    return jsonify({
        'meta': {
            'page': users.page,
            'has_next': users.has_next,
            'has_prev': users.has_prev,
        },
        'data': [{
            'pk': user.pk,
            'login': user.login,
            'grant': user.grant
        } for user in users.items]
    })


@api.route('/get', methods=['GET'])
@utils.login_required
@utils.grant_required
@utils.xhr
@utils.csrf_protect
def get():
    ''' gets one row by pk '''
    pk = request.args.get('pk', 0)
    if not pk:
        abort(404)
    user = User.query.get(pk)
    return jsonify({
        'pk': user.pk,
        'login': user.login,
        'grant': user.grant
    })


@api.route("/insert", methods=['PUT'])
@utils.login_required
@utils.grant_required
@utils.xhr
@utils.csrf_protect
def insert():
    ''' inserts new user '''
    validator = utils.Validator(request.form, {
        'login': ['empty', 'is_string', 'min_length|3', 'max_length|20'],
        'password': ['empty', 'is_string', 'min_length|3', 'max_length|10'],
        'repassword': ['empty', 'is_string', 'is_equal|password'],
        'grant': ['is_bool']
    })
    if not validator.is_valid():
        return jsonify(dict(messages=validator.errors), status_code=400)

    login = request.form.get("login", "")
    password = request.form.get("password", "")
    repassword = request.form.get("repassword", "")
    grant = request.form.get("grant", False)

    # checks if user exist
    if User.query.filter_by(login=login).first():
        return jsonify(dict(messages={
            "login": [u"Пользователь с таким именем уже есть"]
        }), status_code=400)
    # creates new user
    user = User(login, password, grant)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'pk': user.pk,
        'login': user.login,
        'grant': user.grant
    })


@api.route("/delete", methods=['DELETE'])
@utils.login_required
@utils.grant_required
@utils.xhr
@utils.csrf_protect
def delete():
    ''' delete user by pk '''
    pk = request.form.get('pk', None)
    if not pk:
        abort(404)
    user = User.query.get(pk)
    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    return jsonify({})


@api.route("/update", methods=['POST'])
@utils.login_required
@utils.grant_required
@utils.xhr
@utils.csrf_protect
def update():
    ''' updates user '''
    validator = utils.Validator(request.form, {
        'login': ['empty', 'is_string', 'min_length|3', 'max_length|20'],
        'grant': ['is_bool']
    })
    if not validator.is_valid():
        return jsonify(dict(messages=validator.errors), status_code=400)

    pk = request.form.get('pk', None)
    login = request.form.get("login")
    grant = request.form.get("grant", False)

    # checks if pk exist
    if not pk:
        abort(404)
    # check if user with this login exist
    user = User.query.filter_by(login=login)\
        .filter(User.pk != pk).first()
    if user:
        return jsonify(dict(messages={
            'login': [u"Пользователь с таким уже существует"]
        }), status_code=400)
    # gets user by pk
    user = User.query.get(pk)
    if not user:
        abort(404)
    # updates user
    user.login = login
    user.grant = grant
    db.session.commit()

    return jsonify({
        'pk': user.pk,
        'login': user.login,
        'grant': user.grant
    })


@api.route("/new_password", methods=['POST'])
@utils.login_required
@utils.grant_required
@utils.xhr
@utils.csrf_protect
def new_password():
    ''' updates password '''
    validator = utils.Validator(request.form, {
        'password': ['empty', 'is_string', 'min_length|3', 'max_length|10'],
        'repassword': ['empty', 'is_string', 'is_equal|password'],
    })
    if not validator.is_valid():
        return jsonify(dict(messages=validator.errors), status_code=400)
    # checks if pk exist
    pk = request.form.get('pk')
    if not pk:
        abort(404)

    # gets user by pk
    user = User.query.get(pk)
    if not user:
        abort(404)
    # updates password
    user.set_password(request.form.get('password'))

    db.session.commit()

    return jsonify({
        'pk': user.pk,
        'login': user.login,
        'grant': user.grant
    })

# -*- coding: utf-8 -*-
import uuid
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from app.models import User
from app import db, app
from app.utils import csrf_protect

auth = Blueprint('auth', __name__, url_prefix="/auth")


@auth.route('/login', methods=['GET', 'POST'])
@csrf_protect
def login():
    error = ""
    # if method not post - only render
    if request.method == "POST":

        login = request.form.get('login')
        password = request.form.get('password')

        if not login:
            error = u"Поле логин обязательно для заполнения"
        elif not password:
            error = u"Поле пароля обязательно для заполнения"
        else:
            user = User.query.filter_by(login=login).first()
            if not user:
                error = u"Пользователя с таким именем не найдено"
            elif not user.check_password(password):
                error = u"Введен не правильный пароль"
            else:
                # generates user uuid and save it into db
                session['uuid'] = str(uuid.uuid4())
                user.uuid = session['uuid']
                db.session.commit()
                return redirect(url_for("users.list"))
    return render_template('auth/login.html', error=error)


@auth.route("/logout", methods=['GET'])
def logout():
    # remove uuid from session and db
    uuid = session.get('uuid')
    if uuid:
        user = User.query.filter_by(uuid=uuid).first()
        if user:
            user.uuid = ''
            db.session.commit()
    session.clear()
    return redirect(url_for('.login'))

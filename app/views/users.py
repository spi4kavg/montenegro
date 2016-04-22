from flask import Blueprint, render_template, request, redirect, url_for
from app.utils import login_required

users = Blueprint('users', __name__, url_prefix="/users")


@users.route('/list', methods=['GET'])
@login_required
def list():
    return render_template('users/list.html')

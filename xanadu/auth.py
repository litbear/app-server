import functools, logging, os
from flask import (
    Blueprint, g, request, session, jsonify, abort, app
)
from werkzeug.security import check_password_hash, generate_password_hash
import json, logging
from xanadu.models.user import User
from xanadu.commons.util import get_json_arg

bp = Blueprint(__name__, 'auth')

@bp.route('/login', methods=['POST'])
def login():
    username = get_json_arg('username', None)
    password = get_json_arg('password', '')
    if not username:
        return jsonify(status=400, message='username can not empty'), 400
    user = User.query.filter_by(username=username).first()
    # logging.warning(check_password_hash(user.password, 'asdasfas'))
    if user is None:
        return jsonify(status=400, message='wrong with username or password'), 400
    elif not check_password_hash(user.password, password):
        return jsonify(status=400, message='wrong with username or password'), 400
    session['is_login'] = True
    session['user_id'] = user.id
    return jsonify(status=200, data={'token': session.get('session_id')})

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

@bp.route('/logout', methods=['post'])
def logout():
    # session 接口封装的由问题 直接删了
    session['is_login'] = False
    return jsonify(status=200)
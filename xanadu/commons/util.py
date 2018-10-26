from flask import request
import functools, logging
from flask import session, abort, jsonify

def get_json_arg(arg, default):
    try:
        data = request.get_json()
        if data:
            result = data.get(arg, default)
            return result
    except Exception:
        pass
    return default

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('is_login', False):
            return jsonify(status=400, message='you must login first!'), 400
        return view(**kwargs)
    return wrapped_view
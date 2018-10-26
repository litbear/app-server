from flask import Blueprint, g, request, session, jsonify, abort
from xanadu.commons.util import login_required

bp = Blueprint(__name__, 'post')


@bp.route('/posts', methods=['get'])
@login_required
def posts():
    return jsonify(status=200, message='you have logged')
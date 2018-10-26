from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from uuid import uuid4
import json, os, logging

class FileSystemSession(dict, SessionMixin):
    def __init__(self, **args):
        dict.__init__(self, args, modified=False)
    
    def clear(self):
        dict.clear(self)

class FileSystemSessionInterface(SessionInterface):

    def __init__(self, app, permanent=True):
        self.path = os.path.join(app.instance_path, 'sessions')
        self.permanent = permanent
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def open_session(self, app, request):
        # session_id = request.cookies.get(app.session_cookie_name)
        from xanadu.commons.util import get_json_arg
        session_id = request.args.get('token', None) or get_json_arg('token', None)
        # 使用cookies 直接拼文件名是不是安全？
        session_file_path = os.path.join(self.path, '{}.json'.format(session_id))
        if session_id and os.path.exists(session_file_path):
            with open(session_file_path, 'r') as f:
                data = json.load(f)
            if data is not None:
                return FileSystemSession(**data)
            return FileSystemSession(session_id=session_id, permanent=self.permanent)
        else:
            session_id = session_id or str(uuid4())
            return FileSystemSession(session_id=session_id, permanent=self.permanent)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        if not session:
            if session.modified:
                try:
                    os.remove(os.path.join(self.path, session_id))
                except OSError:
                    pass
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain,
                    path=path)
            return
        data = dict(session)
        session_id = data.get('session_id', str(uuid4()))
        with open(os.path.join(self.path, '{}.json'.format(session_id)), 'w+') as f:
            json.dump(data, f, indent=4)
        if session.modified:
            response.set_cookie(
                app.session_cookie_name, 
                session_id,
                expires=expires,
                httponly=httponly,
                domain=domain,
                path=path,
                secure=secure)

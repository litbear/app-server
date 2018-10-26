from flask import Flask, request, abort, jsonify
import os, logging
from xanadu.commons.session import FileSystemSessionInterface
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config=None):
    """创建应用实例 并进一步配置"""
    # instance_relative_config=True tells the app that 
    # configuration files are relative to the instance folder. 
    app = Flask(__name__, instance_relative_config=True)
    
    db_path = os.path.join(app.instance_path, 'database')
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    # 默认配置 可被覆盖
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(db_path, 'xanadu.sqlite')),
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )

    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)

    # 可以通过命令行手动指定配置文件
    # http://flask.pocoo.org/docs/1.0/patterns/appfactories/?highlight=create_app#using-applications
    '''
    if test_config is None:
        # 这里可以根据 config 参数指定配置文件
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    '''

    # 设置日志格式
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S',
    #     filemode='a')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # 设置 session 
    app.session_interface = FileSystemSessionInterface(app)

    # blueprint
    from xanadu.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from xanadu.api import post
    app.register_blueprint(post.bp, url_prefix='/api')

    # database
    db.init_app(app)

    # cli
    from xanadu.commons import cli
    cli.init_app(app)

    ## error handler
    @app.errorhandler(404)
    def err_404(error):
        return jsonify(status=404), 404

    @app.errorhandler(400)
    def err_400(error):
        return jsonify(status=400), 400

    @app.errorhandler(405)
    def err_405(error):
        return jsonify(status=405), 405

    return app
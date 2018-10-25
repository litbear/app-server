from flask import Flask
import os, logging
from xanadu.commons.session import FileSystemSessionInterface
from xanadu.modules.auth.views import bp as auth_bp

def create_app(config=None):
    """创建应用实例 并进一步配置"""
    # instance_relative_config=True tells the app that 
    # configuration files are relative to the instance folder. 
    app = Flask(__name__, instance_relative_config=True)
    
    # 默认配置 可被覆盖
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'xanadu.sqlite'),
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
    app.register_blueprint(auth_bp)

    return app
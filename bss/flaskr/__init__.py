#注册应用程序，后台和db
# Flask应用的run()方法会调用werkzeug.serving模块中的run_simple方法。
# 这个方法会创建一个本地的测试服务器，并且在这个服务器中运行Flask应用。
# 关于服务器的创建这里不做说明，可以查看werkzeug.serving模块的有关文档。
#
# 当服务器开始调用Flask应用后，便会触发Flask应用的__call__(environ,
# start_response)方法。其中environ由服务器产生，
# start_response在服务器中定义。
#
# 上面我们分析到当Flask应用被调用时会执行wsgi_app(environ, start_response)方法
# 。可以看出，wsgi_app是真正被调用的WSGI应用，之所以这样设计，就是为了在应用正式处理请求之前，wsgi_app可以被一些“中间件”装饰，
# 以便先行处理一些操作。为了便于理解，这里先举两个例子进行说明。
from flaskr import auth, blog, theme
from flask import Flask
from . import db
from flaskr.instance.config import config
from .model import User, Post, Theme, Reply


app = Flask(__name__)  # 创建flask应用程序


def create_app(test_config=None):
    app.config.from_object(config)
    app.secret_key = 'super secret key'
    # app.config.from_pyfile('instance/config.py')
    print('即将进入db')
    db.init_db(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(theme.bp)
    #这句话的作用是建立ulr与index连接，
    app.add_url_rule('/', endpoint='indexblog')
    return app



# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from instance.config import config
# # __name__的值为本app文件生成的所在目录；instance_relative_config则假定它们相对于实例路径而不是应用程序根目录。
# #表示从默认模块加载配置
# app = Flask('__name__', instance_relative_config=True)
# app.config.from_object(config)

# #从文件中文件的内容覆盖值去指向默认，以达到设定配置的功能。
# # app.config.from_pyfile('config.py')
# #生成与app有关的sqlalchemy

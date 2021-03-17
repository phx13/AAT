import pymysql
from flask import Flask
from werkzeug.exceptions import HTTPException

from aat_main.utils.api_exception_helper import APIException, InterServerErrorException

pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='views', static_url_path='/', static_folder='resources')
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:phx25891863@localhost:3306/aat?charset=utf8'
app.config['SQLALCHEMY_POOL_SIZE'] = 1000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.errorhandler(Exception)
def catch_http_exception(e):
    if isinstance(e, HTTPException):
        api_exception = APIException(e.code, e.description)
    else:
        api_exception = InterServerErrorException()
    return render_template('error.html', api_exception=api_exception)


@app.before_request
def before_request():
    pass


from aat_main.controllers.index_controller import *

app.register_blueprint(index_blueprint)

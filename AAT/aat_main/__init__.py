import pymysql
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
import os

from aat_main.utils.api_exception_helper import APIException, InterServerErrorException

pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='views', static_url_path='/', static_folder='resources')
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/aat?charset=utf8'
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
from aat_main.controllers.course_controller import *
from aat_main.controllers.summative_controller import *

app.register_blueprint(index_blueprint)
app.register_blueprint(course_blueprint)
app.register_blueprint(summative_blueprint)

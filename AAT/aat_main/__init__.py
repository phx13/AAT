import pymysql
from flask import Flask, render_template, request, session

pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='views', static_url_path='/', static_folder='resources')
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/cw2?charset=utf8'
app.config['SQLALCHEMY_POOL_SIZE'] = 1000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.errorhandler(404)
def error404(e):
    return render_template('error404.html')


@app.errorhandler(500)
def error500(e):
    return render_template('error500.html')


@app.before_request
def before_request():
    pass
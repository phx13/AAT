from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    return render_template('login.html')

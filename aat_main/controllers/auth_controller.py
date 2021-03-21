from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from aat_main.forms.auth_forms import LoginForm
from aat_main import db
from aat_main.models.account_model import AccountModel

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_bp.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(AccountModel).filter_by(email=form.email.data).first()
        if not user or not user.password == form.password.data:  # maybe change this to not (... and ...)
            flash('Email or password is incorrect.')
            return render_template('login.html', title='Log In', form=form)
        login_user(user, remember=True)
        return redirect(url_for('index_bp.home'))

    return render_template('login.html', title='Log In', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index_bp.home'))

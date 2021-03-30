import hashlib

from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, logout_user

from aat_main.forms.auth_forms import LoginForm
from aat_main.models.account_model import AccountModel
from aat_main.utils.pillow_helper import ImageCaptchaHelper
from aat_main.utils.random_helper import RandomHelper
from aat_main.utils.smtp_helper import EmailHelper

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_bp.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = AccountModel.search_account_by_email(form.email.data)

        # if form.login_captcha.data.lower().strip() != session.get('login_captcha'):
        #     flash('Fail (Server) : Incorrect login captcha')
        #     return render_template('login.html', title='Log In', form=form)
        if not user:
            flash('Fail (Server) : Account does not exist')
            return render_template('login.html', title='Log In', form=form)
        elif form.password.data != user.password:
            flash('Fail (Server) : Password is wrong')
            return render_template('login.html', title='Log In', form=form)

        login_user(user, remember=True)

        if next_url := request.args.get('next'):
            return redirect(next_url)

        return redirect(url_for('index_bp.home'))

    return render_template('login.html', title='Log In', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/login/captcha/')
def login_captcha():
    try:
        code, base64_str = ImageCaptchaHelper().get_image_captcha()
        session['login_captcha'] = code.lower()
        return base64_str
    except:
        return 'Fail (Server) : Login captcha generate failed'


@auth_bp.route('/login/password/', methods=['POST'])
def login_password():
    try:
        email = request.form.get('email').strip()
        user = AccountModel.search_account_by_email(email)
        if not user:
            return 'Fail (Server) : Account is not existed'

        password = RandomHelper.generate_code(5)
        subject = 'Reset password for AAT'
        content = f"<br/>Welcome to login AAT, your password is reset as <span style='color:orange;'>{password}</span>"
        receiver_email = email
        sender_name = 'AAT team'
        sender_email = 'aat@cs.cf.ac.uk'
        EmailHelper.send_email(subject, content, receiver_email, sender_name, sender_email)

        password = hashlib.md5(password.encode()).hexdigest()
        AccountModel().update_account(email, user.id, password, user.name)
        return 'Success (Server) : Reset password successful'
    except:
        return 'Fail (Server) : Email send failed'

import hashlib
import time

from flask import Blueprint, request, render_template
from flask_login import current_user

from aat_main.models.account_model import AccountModel
from aat_main.utils.base64_helper import Base64Helper

account_bp = Blueprint('account_bp', __name__, template_folder='../views/account_management')


@account_bp.route('/account/')
def account_page():
    try:
        current_account = AccountModel.search_account_by_email(current_user.email)
        if current_account:
            return render_template('account_base.html', current_account=current_account)
        if not current_account:
            return 'Fail (Server) : Account is not existed'
    except:
        return 'Fail (Server) : Account page init failed'


@account_bp.route('/account/profile/', methods=['POST'])
def update_profile():
    try:
        current_account = AccountModel.search_account_by_email(current_user.email)
        avatar = request.form.get('avatar')
        name = request.form.get('name')
        password = request.form.get('password')
        profile = request.form.get('profile')

        if avatar.startswith("data:image/"):
            avatar = Base64Helper.base64_to_picture(avatar, 'avatars/' + current_user.email + '.jpg')
        else:
            avatar = current_account.avatar

        if password == '':
            password = current_account.password
        else:
            password = hashlib.md5(password.encode()).hexdigest()

        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        AccountModel.update_account(current_account.email, current_account.id, password, name, current_account.role, avatar, profile, update_time)
        return 'Success (Server) : Update profile successful'
    except:
        return 'Fail (Server) : Update profile failed'

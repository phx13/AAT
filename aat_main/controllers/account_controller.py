import hashlib
import time

from flask import Blueprint, request, render_template
from flask_login import current_user, login_required
from jinja2 import TemplateError
from sqlalchemy.exc import SQLAlchemyError

from aat_main.models.account_model import AccountModel
from aat_main.models.course_model import CourseModel
from aat_main.utils.api_exception_helper import InterServerErrorException, NotFoundException
from aat_main.utils.base64_helper import Base64Helper

account_bp = Blueprint('account_bp', __name__, template_folder='../views/account_management')


@account_bp.before_request
@login_required
def before_request():
    pass


@account_bp.route('/account/')
def account_page():
    try:
        courses = CourseModel.search_courses_by_email(current_user.email).split(',')
        return render_template('account_base.html', current_account=current_user, courses=courses, student_stat_status=0)
    except TemplateError:
        raise NotFoundException()


@account_bp.route('/account/profile/', methods=['POST'])
def update_profile():
    try:
        avatar = request.form.get('avatar')
        name = request.form.get('name')
        password = request.form.get('password')
        profile = request.form.get('profile')

        if avatar.startswith("data:image/"):
            avatar = Base64Helper.base64_to_picture(avatar, 'avatars/' + current_user.email + '.jpg')
        else:
            avatar = current_user.avatar

        if password == '':
            password = current_user.password
        else:
            password = hashlib.md5(password.encode()).hexdigest()

        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        AccountModel.update_account(current_user.email, current_user.id, password, name, current_user.role, avatar, profile, update_time)
        return 'Success (Server) : Update profile successful'
    except SQLAlchemyError:
        raise InterServerErrorException()


@account_bp.route('/account/stat/attempt/<string:course>/')
def stat_attempt(course):
    return render_template('account_base.html', current_account=current_user, course=course, student_stat_status=1)


@account_bp.route('/account/stat/attainment/<string:course>/')
def stat_attainment(course):
    return render_template('account_base.html', current_account=current_user, course=course, student_stat_status=2)


@account_bp.route('/account/stat/engagement/<string:course>/')
def stat_engagement(course):
    return render_template('account_base.html', current_account=current_user, course=course, student_stat_status=3)
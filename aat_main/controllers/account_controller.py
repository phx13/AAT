import hashlib
import time
from statistics import mean

from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user, login_required
from jinja2 import TemplateError
from sqlalchemy.exc import SQLAlchemyError

from aat_main.models.account_model import AccountModel
from aat_main.models.assessment_models import Assessment, AssessmentCompletion
from aat_main.models.credit_model import CreditModel
from aat_main.utils.api_exception_helper import InterServerErrorException, NotFoundException
from aat_main.utils.base64_helper import Base64Helper
from aat_main.utils.serialization_helper import SerializationHelper

account_bp = Blueprint('account_bp', __name__, template_folder='../views/account_management')


@account_bp.before_request
@login_required
def before_request():
    pass


@account_bp.route('/account/')
def account_page():
    try:
        courses = current_user.get_enrolled_module_codes()
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


@account_bp.route('/account/stat/attempt/data/')
def stat_attempt_data():
    conditions = []
    if ('module' in request.args) and (request.args['module']):
        conditions.append(Assessment.module == request.args['module'])

    if ('type' in request.args) and (request.args['type']):
        if request.args['type'] == '0' or request.args['type'] == '1':
            conditions.append(Assessment.type == request.args['type'])

    if ('startDate' in request.args) and (request.args['startDate']):
        conditions.append(AssessmentCompletion.submit_time > request.args['startDate'])

    if ('endDate' in request.args) and (request.args['endDate']):
        conditions.append(AssessmentCompletion.submit_time < request.args['endDate'])

    if current_user.role == 'student':
        conditions.append(AssessmentCompletion.student_id == current_user.id)

    score = AssessmentCompletion.get_score_by_conditions(*conditions)
    return jsonify(SerializationHelper.model_to_list(score))


@account_bp.route('/account/stat/attainment/<string:course>/')
def stat_attainment(course):
    return render_template('account_base.html', current_account=current_user, course=course, student_stat_status=2)


@account_bp.route('/account/stat/attainment/data/')
def stat_attainment_data():
    conditions = []
    if ('module' in request.args) and (request.args['module']):
        conditions.append(Assessment.module == request.args['module'])

    if current_user.role == 'student':
        conditions.append(AssessmentCompletion.student_id == current_user.id)

    formative_score_avg = AssessmentCompletion.get_score_avg_by_conditions(*conditions, Assessment.type == '0').scalar()
    if not formative_score_avg:
        formative_score_avg = 0
    summative_score_avg = AssessmentCompletion.get_score_avg_by_conditions(*conditions, Assessment.type == '1').scalar()
    if not summative_score_avg:
        summative_score_avg = 0
    # TODO How to express formative_accuracy summative_accuracy?
    formative_accuracy = AssessmentCompletion.get_t1_accuracy_by_conditions(*conditions).scalar()
    if not formative_accuracy:
        formative_accuracy = 0
    summative_accuracy = AssessmentCompletion.get_t2_accuracy_by_conditions(*conditions).scalar()
    if not summative_accuracy:
        summative_accuracy = 0
    knowledge_level = mean([formative_score_avg, summative_score_avg, formative_accuracy, summative_accuracy])

    datas = [str(round(knowledge_level, 2)), str(round(formative_score_avg, 2)), str(round(summative_score_avg, 2)), str(round(formative_accuracy, 2) * 100) + '%',
             str(round(summative_accuracy, 2) * 100) + '%']
    return jsonify(datas)


@account_bp.route('/account/stat/engagement/<string:course>/')
def stat_engagement(course):
    return render_template('account_base.html', current_account=current_user, course=course, student_stat_status=3)


@account_bp.route('/account/stat/engagement/data/')
def stat_engagement_data():
    conditions = []
    if ('module' in request.args) and (request.args['module']):
        conditions.append(Assessment.module == request.args['module'])

    if current_user.role == 'student':
        conditions.append(CreditModel.account_id == current_user.id)

    credit_types = CreditModel.get_types_by_conditions(*conditions)
    module_credit = str(CreditModel.get_credit_by_conditions(*conditions).scalar())
    if module_credit == 'None':
        module_credit = '0'
    credit_dic = {}
    credit_dic.update({5: module_credit})
    for credit_type in credit_types:
        credit = str(CreditModel.get_credit_by_conditions(*conditions, CreditModel.type == credit_type[0]).scalar())
        if credit == 'None' or credit == 'NaN':
            credit = '0'
        dic = {credit_type[0]: credit}
        credit_dic.update(dic)
    return jsonify(credit_dic)


@account_bp.route('/account/stat/credit/data/')
def stat_credit_data():
    origin_data = CreditModel.get_credit_by_account_id(current_user.id)
    data = []
    for od in origin_data:
        dic = {
            'id': od.id,
            'event': od.event,
            'credit': od.credit,
            'time': od.time
        }
        data.append(dic)
    return jsonify(data)

from flask import Blueprint, render_template

error_bp = Blueprint('error_blueprint', __name__, url_prefix='/error', template_folder='../views/errors')


@error_bp.app_errorhandler(404)
def error404(e):
    print(e)
    return render_template('error404.html')


@error_bp.app_errorhandler(500)
def error500(e):
    print(e)
    return render_template('error505.html')

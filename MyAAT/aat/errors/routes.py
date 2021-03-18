from flask import render_template
from aat.errors import bp

@bp.app_errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def error500(e):
    return render_template('500.html'), 500


from flask import render_template, current_app, send_from_directory
from aat.main import bp


@bp.route('/index')
@bp.route('/home')
@bp.route('/')
def home():
    print(current_app.config['SECRET_KEY'])
    return render_template('home.html', title='Home')
#
#
# @bp.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(current_app.root_path, 'static'),
#                                'img/favicon.ico', mimetype='image/vnd.microsoft.icon')
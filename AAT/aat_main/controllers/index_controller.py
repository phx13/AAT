from flask import Blueprint, render_template, abort

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/')
def index_page():
    try:
        return render_template('index.html')
    except:
        abort(404)

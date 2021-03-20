from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__, static_folder='resources')


@index_bp.route('/home')
@index_bp.route('/')
def home():
    return render_template('index.html')

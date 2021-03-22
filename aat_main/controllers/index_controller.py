from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__, static_folder='resources')


@index_bp.route('/home')
@index_bp.route('/')
def home():
    return render_template('index.html')


@index_bp.route('/echarts/')
def echarts():
    return render_template('echarts.html')
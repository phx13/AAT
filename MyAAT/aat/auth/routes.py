from flask import redirect, url_for, render_template

from aat.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Log In')


@bp.route('/logout')
def logout():
    return redirect(url_for('main.home'))

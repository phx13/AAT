from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


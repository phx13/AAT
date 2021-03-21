from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

from flask import redirect, url_for
from flask_login import UserMixin
from aat_main import db, login_manager
from aat_main.utils.api_exception_helper import InterServerErrorException
from aat_main.models.assessment_models import Assessment, AssessmentCompletion


class AccountModel(db.Model, UserMixin):
    __tablename__ = 'account'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(128), unique=True, nullable=False)
    # password = db.Column(db.String(128), nullable=False)
    # name = db.Column(db.String(64), nullable=False)

    @staticmethod
    def search_account_by_id(id):
        try:
            return db.session.query(AccountModel).filter_by(id=id).first()
        except SQLAlchemyError:
            return InterServerErrorException()

    @staticmethod
    def create_account(id, email, password, name):
        try:
            db.session.add(AccountModel(id=id, email=email, password=password, name=name))
            db.session.commit()
        except SQLAlchemyError:
            return InterServerErrorException()

    def update_account(self, id, email, password, name):
        try:
            self.search_account_by_id(id).update({'email': email, 'password': password, 'name': name})
            db.session.commit()
        except SQLAlchemyError:
            return InterServerErrorException()

    def delete_account(self, id):
        try:
            self.search_account_by_id(id).delete()
            db.session.commit()
        except SQLAlchemyError:
            return InterServerErrorException()

    def get_completed_assessments(self):
        return db.session.query(
            Assessment
        ).join(
            AssessmentCompletion,
            Assessment.id == AssessmentCompletion.assessment_id
        ).filter(
            AssessmentCompletion.student_id == self.id
        ).all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(AccountModel).get(int(user_id))

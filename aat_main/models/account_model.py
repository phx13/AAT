from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

from aat_main import db
from aat_main.utils.api_exception_helper import InterServerErrorException


class AccountModel(db.Model):
    __tablename__ = 'account'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)

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

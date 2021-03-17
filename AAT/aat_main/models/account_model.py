from sqlalchemy import MetaData, Table

from aat_main import db
from aat_main.utils.api_exception_helper import InterServerErrorException


class AccountModel(db.Model):
    __tablename__ = 'account'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)

    def search_account_by_id(self, id):
        try:
            return db.session.query(AccountModel).filter_by(id=id).first()
        except:
            return InterServerErrorException()

    def create_account(self, id, email, password, name):
        try:
            account_model = AccountModel(id=id, email=email, password=password, name=name)
            db.session.add(account_model)
            db.session.commit()
        except:
            return InterServerErrorException()

    def update_account(self, id, email, password, name):
        try:
            self.search_account_by_id(id).update({'email': email, 'password': password, 'name': name})
            db.session.commit()
        except:
            return InterServerErrorException()

    def delete_account(self, id):
        try:
            self.search_account_by_id(id).delete()
            db.session.commit()
        except:
            return InterServerErrorException()

from sqlalchemy import MetaData, Table, func

from aat_main import db


class CreditModel(db.Model):
    __tablename__ = 'credit'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int
    email: varchar
    type: varchar
    event: varchar
    target: int
    credit: int
    time: datetime
    """

    @staticmethod
    def get_credit_by_email(email):
        return db.session.query(CreditModel).filter_by(email=email).order_by(CreditModel.time.desc()).all()

    @staticmethod
    def get_types_by_email(email):
        return db.session.query(CreditModel.type).filter_by(email=email).distinct().all()

    @staticmethod
    def get_credit_by_email_and_type(email, type):
        return db.session.query(func.sum(CreditModel.credit)).filter_by(email=email, type=type)

    @staticmethod
    def insert_credit(email, type, event, target, credit, time):
        db.session.add(CreditModel(email=email, type=type, event=event, target=target, credit=credit, time=time))
        db.session.commit()

    @staticmethod
    def check_credit(email, type, target):
        return db.session.query(CreditModel).filter_by(email=email, type=type, target=target).first()

    @staticmethod
    def check_credit_by_time(email, type, start_time, end_time):
        return db.session.query(CreditModel).filter(CreditModel.email == email, CreditModel.type == type, CreditModel.time.between(start_time, end_time)).all()

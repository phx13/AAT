from sqlalchemy import MetaData, Table

from aat_main import db


class Module(db.Model):
    __tablename__ = 'module'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    code: varchar(8), primary
    name: varchar(128)
    """

    @staticmethod
    def get_all():
        return db.session.query(Module).all()

    @staticmethod
    def get_module_by_id(id):
        return db.session.query(Module).get(id)

    @staticmethod
    def create_module(code, name):
        db.session.add(Module(code=code, name=name))
        db.session.commit()

from sqlalchemy import MetaData, Table

from aat_main import db


class Question(db.Model):
    __tablename__ = 'question'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment, primary
    name: varchar(128)
    description: varchar(256)
    module_id: int, foreign key
    """

    @staticmethod
    def get_question_by_id(id):
        return db.session.query(Question).get(id)

    @staticmethod
    def create_question(name, description, module_id):
        db.session.add(Question(name=name, description=description, module_id=module_id))
        db.session.commit()

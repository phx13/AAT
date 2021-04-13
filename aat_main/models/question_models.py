from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

from aat_main import db

class Question(db.Model):
    __tablename__ = 'question'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment, primary
    name: varchar(128)
    description: varchar(256)
    course: varchar(64)
    """

    @staticmethod
    def get_question_by_id(id):
        return db.session.query(Question).get(id)

    def create_question(name, description, course):
        db.session.add(Question(name=name, description=description, course=course))
        db.session.commit()


class QuestionData(db.Model):
    __tablename__ = 'questiondata'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment, primary
    name: varchar(128)
    description: varchar(256)
    course: varchar(64)
    """


    @staticmethod
    def search_all():
        return db.session.query(QuestionData).all()

    @staticmethod
    def delete_question_by_id(id):
        try:
            db.session.query(QuestionData).filter_by(id=id).delete()
            db.session.commit()
        except SQLAlchemyError:
            return 'Server error'

    @staticmethod
    def get_question_by_id(id):
        return db.session.query(Question).get(id)

    def create_question(name, description, course):
        db.session.add(Question(name=name, description=description, course=course))
        db.session.commit()
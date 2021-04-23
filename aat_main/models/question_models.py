from flask_login import current_user
from sqlalchemy import MetaData, Table, or_
from sqlalchemy.exc import SQLAlchemyError

from aat_main import db
from aat_main.models.module_model import Module
from aat_main.models.satisfaction_review_model import QuestionReview


# type one question
class MultipleChoice(db.Model):
    __tablename__ = 'MultipleChoice'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)

    """
    id: int, auto_increment, primary
    question: varchar(256)
    answer: varchar(256)
    options: varchar(64)
    """

    @staticmethod
    def search_question_by_id(id):
        return db.session.query(MultipleChoice).filter_by(id=id).first()

    @staticmethod
    def create_question(question, answer, options):
        db.session.add(MultipleChoice(question=question, answer=answer, options=options))
        db.session.commit()

    def update_question(self, id, question, answer, options):
        self.search_question_by_id(id).update({'question': question, 'answer': answer, 'options': options})
        db.session.commit()

    def delete_question(self, id):
        self.search_question_by_id(id).delete()
        db.session.commit()

# type two question
class FillinBlank(db.Model):
    __tablename__ = 'FillinBlank'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)

    """
    id: int, auto_increment, primary
    name: varchar(128)
    description: varchar(256)
    module_code: varchar, foreign key\
    type: int, formative-multiple choice:0; formative-fill in blank:1; summative:2
    option: varchar(128)
    answer: varchar(128)
    release_time: datetime
    """

    @staticmethod
    def get_all():
        return db.session.query(Question).all()

    def get_question_by_id(id):
        return db.session.query(Question).get(id)

    @staticmethod
    def get_question_by_module(module):
        return db.session.query(Question).filter(Question.module_code == module).all()

    @staticmethod
    def get_question_by_all_module():
        modules = current_user.get_enrolled_modules()
        conditions = [Question.module_code == mc.code for mc in modules]
        return db.session.query(Question).filter(or_(*conditions)).all()

    @staticmethod
    def create_question(name, description, module_code):
        db.session.add(Question(name=name, description=description, module_code=module_code))
        db.session.commit()

    @staticmethod
    def create_question_management(module_code, name, type, description, option, answer):
        db.session.add(Question(module_code=module_code, name=name, type=type, description=description, option=option, answer=answer))
        db.session.commit()

    @staticmethod
    def delete_question_by_id(id):
        try:
            db.session.query(Question).filter_by(id=id).delete()
            db.session.commit()
        except SQLAlchemyError:
            return 'Server error'

    def get_module(self):
        return db.session.query(
            Module
        ).filter_by(
            code=self.module_code
        ).first()

    def get_reviews(self):
        return db.session.query(
            QuestionReview
        ).filter_by(
            question_id=self.id
        ).all()
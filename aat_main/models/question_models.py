from sqlalchemy import MetaData, Table

from aat_main import db
from aat_main.models.module_model import Module
from aat_main.models.satisfaction_review_model import QuestionReview


class Question(db.Model):
    __tablename__ = 'question'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment, primary
    name: varchar(128)
    description: varchar(256)
    module_code: int, foreign key
    """

    @staticmethod
    def get_question_by_id(id):
        return db.session.query(Question).get(id)

    @staticmethod
    def create_question(name, description, module_code):
        db.session.add(Question(name=name, description=description, module_code=module_code))
        db.session.commit()

    def get_module(self):
        return db.session.query(
            Module
        ).filter_by(
            code=self.module
        ).first()

    def get_reviews(self):
        return db.session.query(QuestionReview).filter_by(question_id=self.id)
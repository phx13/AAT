from sqlalchemy import MetaData, Table

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
    def get_questions():
        return db.session.query(Question).all()
        
    def get_question_by_id(id):
        return db.session.query(Question).get(id)

    def create_question(name, description, course):
        db.session.add(Question(name=name, description=description, course=course))
        db.session.commit()
from sqlalchemy import MetaData, Table

from aat_main import db

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
    question: varchar(256)
    answer: varchar(256)
    caseSenstive: Boolean
    """

    @staticmethod
    def search_question_by_id(id):
        return db.session.query(FillinBlank).filter_by(id=id).first()

    @staticmethod
    def create_question(question, answer, caseSensetive):
        db.session.add(FillinBlank(question=question, answer=answer, caseSensetive=caseSensetive))
        db.session.commit()

    def update_question(self, id, question, answer, caseSensetive):
        self.search_question_by_id(id).update({'question': question, 'answer': answer, 'caseSensetive': caseSensetive})
        db.session.commit()

    def delete_question(self, id):
        self.search_question_by_id(id).delete()
        db.session.commit()
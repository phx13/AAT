from sqlalchemy import MetaData, Table

from aat_main import db


class AssessmentReview(db.Model):
    __tablename__ = 'assessment_review'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment
    student_id: int, foreign key
    assessment_id: int, foreign key
    statement1_answer: int
    statement2_answer: int
    comment: text
    """

    @staticmethod
    def create_review(student_id, assessment_id, statement1_answer, statement2_answer, comment):
        db.session.add(AssessmentReview(student_id=student_id, assessment_id=assessment_id,
                                        statement1_answer=statement1_answer, statement2_answer=statement2_answer,
                                        comment=comment))
        db.session.commit()


class AATReview(db.Model):
    __tablename__ = 'aat_review'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment
    student_id: int, foreign key
    statement1_answer: int
    statement2_answer: int
    comment: text
    """

    @staticmethod
    def create_review(student_id, statement1_answer, statement2_answer, comment):
        db.session.add(AATReview(student_id=student_id, statement1_answer=statement1_answer,
                                        statement2_answer=statement2_answer, comment=comment))
        db.session.commit()

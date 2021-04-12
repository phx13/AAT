from sqlalchemy import MetaData, Table

from aat_main import db
from aat_main.models.satisfaction_review_model import AssessmentReview


class Assessment(db.Model):
    __tablename__ = 'assessment'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment, primary
    name: varchar(64)
    description: text
    course: varchar(64)
    questions: varchar(256)
    """

    @staticmethod
    def get_assessment_by_id(id):
        return db.session.query(Assessment).get(id)

    def get_reviews(self):
        return db.session.query(AssessmentReview).filter_by(assessment_id=self.id).all()

    def create_assessment(title, questions, description, course):
        question_string = generate_question_string(questions)
        db.session.add(Assessment(name=title, questions=question_string, description=description, course=course))
        db.session.commit()

    def generate_question_string(questions):
        question_string = ""
        count = 0
        while count < (len(questions) - 1):
            temp = questions[count]
            question_string.append(str(temp) + "&")
            count+=1
        temp = questions[count]
        question_string.append(str(temp))
        return question_string
        

class AssessmentCompletion(db.Model):
    __tablename__ = 'assessment_completion'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment
    student_id: foreign key, references account(id)
    assessment_id: foreign key, references assessment(id)
    """

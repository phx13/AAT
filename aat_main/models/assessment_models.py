from sqlalchemy import MetaData, Table

from aat_main import db
from aat_main.models.satisfaction_review_model import AssessmentReview


class Assessment(db.Model):
    __tablename__ = 'assessment'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment, primary
    title: varchar(64)
    description: text
    module: varchar(8), foreign key references module(code)
    questions: varchar(256)
    availability_date: datetime
    due_date: datetime
    timelimit: int
    time_created: datetime, default now()
    """

    @staticmethod
    def get_assessment_by_id(id):
        return db.session.query(Assessment).get(id)

    def get_reviews(self):
        return db.session.query(AssessmentReview).filter_by(assessment_id=self.id).all()

    def convert_datetime(date, time):
        return str(date) + " " + str(time)

    def create_assessment(title, questions, description, module, start_datetime, end_datetime, timelimit):
        db.session.add(Assessment(title=title, questions=questions, description=description, module=module,
                                  availability_date=start_datetime, due_date=end_datetime, timelimit=timelimit))
        db.session.commit()


class AssessmentCompletion(db.Model):
    __tablename__ = 'assessment_completion'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, auto_increment
    student_id: foreign key, references account(id)
    assessment_id: foreign key, references assessment(id)
    """

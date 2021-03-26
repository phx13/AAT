from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import MetaData, Table, and_

from aat_main import db, login_manager
from aat_main.models.assessment_models import Assessment, AssessmentCompletion
from aat_main.models.satisfaction_review_models import AssessmentReview, AATReview


class AccountModel(db.Model, UserMixin):
    __tablename__ = 'account'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, primary key, auto_increment
    email: varchar(128)
    password: varchar(128)
    name: varchar(64)
    role: varchar(16) (either student, lecturer, or admin)
    """

    @staticmethod
    def search_all():
        return db.session.query(AccountModel).all()

    @staticmethod
    def search_account_by_id(id):
        return db.session.query(AccountModel).get(id)

    @staticmethod
    def search_account_by_email(email):
        return db.session.query(AccountModel).filter_by(email=email).first()

    @staticmethod
    def create_account(id, email, password, name):
        db.session.add(AccountModel(id=id, email=email, password=password, name=name))
        db.session.commit()

    @staticmethod
    def update_account(email, id, password, name):
        db.session.query(AccountModel).filter_by(email=email).update({'id': id, 'password': password, 'name': name})
        db.session.commit()

    def delete_account(self, id):
        self.search_account_by_id(id).delete()
        db.session.commit()

    def get_completed_assessments(self):
        return db.session.query(
            Assessment
        ).join(
            AssessmentCompletion,
            Assessment.id == AssessmentCompletion.assessment_id
        ).filter(
            AssessmentCompletion.student_id == self.id
        ).all()

    def has_reviewed_assessment(self, id):
        return db.session.query(
            AssessmentReview
        ).filter(
            and_(
                AssessmentReview.student_id == self.id,
                AssessmentReview.assessment_id == id
            )
        ).first()

    def get_last_aat_review(self):
        return db.session.query(AATReview).filter_by(student_id=self.id).order_by(AATReview.date.desc()).first()

    # reference https://stackoverflow.com/questions/46046136/find-out-if-a-date-is-more-than-30-days-old/46046182#46046182
    # 21 March
    def has_reviewed_aat_recently(self):
        if (last_review := self.get_last_aat_review()) is None:
            return False
        else:
            time_elapsed = datetime.now() - last_review.date
            return time_elapsed.days < 7

    def get_days_until_next_aat_review(self):
        last_review_date = self.get_last_aat_review().date
        time_elapsed = datetime.now() - last_review_date
        return 7 - time_elapsed.days


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(AccountModel).get(int(user_id))

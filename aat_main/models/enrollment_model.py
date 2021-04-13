from sqlalchemy import MetaData, Table

from aat_main import db


class StudentEnrolment(db.Model):
    __tablename__ = 'student_enrolment'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, primary key, auto_increment
    student_id: int, foreign key
    module_code: varchar(8), foreign key
    """

    @staticmethod
    def get_enrolled_modules(student_id):
        return db.session.query(StudentEnrolment).filter_by(student_id=student_id).all()

    @staticmethod
    def get_enrolled_students(module_id):
        return db.session.query(StudentEnrolment).filter_by(module_id=module_id).all()

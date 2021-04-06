from sqlalchemy import MetaData, Table

from aat_main import db


class CourseModel(db.Model):
    __tablename__ = 'course'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, primary key, auto_increment
    email: varchar(128)
    courses: varchar(128)
    """

    @staticmethod
    def search_courses_by_email(email):
        return db.session.query(CourseModel).filter_by(email=email).first().courses

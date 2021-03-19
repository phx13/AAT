from sqlalchemy import MetaData, Table

from aat_main import db


class CourseModel(db.Model):
    __tablename__ = 'course'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)

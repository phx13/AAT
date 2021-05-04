from sqlalchemy import MetaData, Table

from aat_main import db
from aat_main.models.assessment_models import Assessment


class ScoreModel(db.Model):
    __tablename__ = 'score'
    __table__ = Table(__tablename__, MetaData(bind=db.engine), autoload=True)
    """
    id: int, primary_key, autoincrement
    assessment_id: int
    account_id: int
    attempt: int
    score: int
    time_cost: int
    submit_time: datetime
    """

    @staticmethod
    def get_score_by_module(account_id, module):
        return db.session.query(ScoreModel).join(Assessment, Assessment.module == module).filter(ScoreModel.account_id == account_id,
                                                                                                 ScoreModel.assessment_id == Assessment.id).all()

    @staticmethod
    def get_score_by_module_and_type(account_id, module, type):
        return db.session.query(ScoreModel).join(Assessment, Assessment.module == module).filter(ScoreModel.account_id == account_id,
                                                                                                 ScoreModel.assessment_id == Assessment.id,
                                                                                                 Assessment.type == type).all()

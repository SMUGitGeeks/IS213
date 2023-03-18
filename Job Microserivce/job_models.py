from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


# Define the Job model and its fields
class Job(db.Model):
    __tablename__ = 'Job'
    job_id = db.Column(db.String(10), primary_key=True, nullable=False)
    job_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "job_name": self.job_name
        }


# Define the JobSkill model and its fields
# JobSkill is in a relationship with Job
class JobSkill(db.Model):
    __tablename__ = 'JobSkill'
    job_id = db.Column(db.String(10), db.ForeignKey('Job.job_id'), primary_key=True, nullable=False)
    skill_name = db.Column(db.String(50), primary_key=True, nullable=False)
    job = db.relationship("Job", backref=backref("Job", uselist=False))

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "skill_name": self.skill_name
        }

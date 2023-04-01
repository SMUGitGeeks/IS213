from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


# Define the Job model and its fields
class Job(db.Model):
    __tablename__ = 'Job'
    job_id = db.Column(db.Integer, primary_key=True, nullable=False)
    job_role = db.Column(db.String(50), nullable=False)
    job_company = db.Column(db.String(50), nullable=False)
    job_description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "job_role": self.job_role,
            "job_company": self.job_company,
            "job_description": self.job_description
        }


# Define the JobSkill model and its fields
# JobSkill is in a relationship with Job
class JobSkill(db.Model):
    __tablename__ = 'JobSkill'
    job_id = db.Column(db.Integer, db.ForeignKey('Job.job_id'), primary_key=True, nullable=False)
    skill_name = db.Column(db.String(50), primary_key=True, nullable=False)
    job = db.relationship("Job", backref=backref("Job", uselist=False))

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "skill_name": self.skill_name
        }

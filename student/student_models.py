from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


# Define the Module model and its fields
class Student(db.Model):
    __tablename__ = 'Student'

    student_id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    is_subscribed = db.Column(db.SmallInteger, nullable=False)
    is_graduated = db.Column(db.SmallInteger, nullable=False)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "student_name": self.student_name,
            "email": self.email,
            "is_graduated": self.is_graduated,
            "is_subscribed": self.is_subscribed}


# Define the ModuleSkill model and its fields
# ModuleSkill is in a relationship with Module
class StudentModule(db.Model):
    __tablename__ = 'Studentmodule'
    student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'), primary_key=True, nullable=False)
    module_id = db.Column(db.String(10), primary_key=True, nullable=False)
    module = db.relationship("Student", backref=backref("Student", uselist=False))

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "module_id": self.module_id
        }

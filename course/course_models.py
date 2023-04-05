from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


# Define the Course model and its fields
class Course(db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(db.String(10), primary_key=True, nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    course_link = db.Column(db.String(400), nullable=False)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_link": self.course_link

        }


# Define the CourseSkill model and its fields
# CourseSkill is in a relationship with Course
class CourseSkill(db.Model):
    __tablename__ = 'CourseSkill'
    course_id = db.Column(db.String(10), db.ForeignKey('Course.course_id'), primary_key=True, nullable=False)
    skill_name = db.Column(db.String(50), primary_key=True, nullable=False)
    course = db.relationship("Course", backref=backref("Course", uselist=False))

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "skill_name": self.skill_name
        }

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


# Define the Module model and its fields
class Module(db.Model):
    __tablename__ = 'Module'
    module_id = db.Column(db.String(10), primary_key=True, nullable=False)
    module_name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "module_id": self.module_id,
            "module_name": self.module_name
        }


# Define the ModuleSkill model and its fields
# ModuleSkill is in a relationship with Module
class ModuleSkill(db.Model):
    __tablename__ = 'ModuleSkill'
    module_id = db.Column(db.String(10), db.ForeignKey('Module.module_id'), primary_key=True, nullable=False)
    skill_name = db.Column(db.String(100), primary_key=True, nullable=False)
    module = db.relationship("Module", backref=backref("Module", uselist=False))

    def to_dict(self):
        return {
            "module_id": self.module_id,
            "skill_name": self.skill_name
        }

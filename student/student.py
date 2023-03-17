import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)

class Student(db.Model):
    __tablename__ = 'student'


    student_id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    is_subscribed = db.Column(db.SmallInteger, nullable=False)
    is_graduated = db.Column(db.SmallInteger, nullable=False)


    def __init__(self, student_id, student_name, email, is_subscribed, is_graduated):
        self.student_id = student_id
        self.student_name = student_name
        self.email = email
        self.is_subscribed = is_subscribed
        self.is_graduated = is_graduated


    def json(self):
        return {"student_id": self.student_id, "name": self.student_name, "email": self.email, "grad": self.is_graduated, "sub": self.is_subscribed}

@app.route("/students/<string:student_id>/modules")
def list_modules_by_id(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        return jsonify(
            {
                "code": 200,
                "data": student.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "student_id": student_id
            },
            "message": "student not found."
        }
    ), 404

@app.route("/")
def home():
    return "hello"

if __name__ == '__main__':
    app.run(port=5200, debug=True)
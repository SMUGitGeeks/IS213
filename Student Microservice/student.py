# import os
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
# # dialect+driver://username:password@host:port/database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# CORS(app)

# class Student(db.Model):
#     __tablename__ = 'student'


#     student_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     student_name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     is_subscribed = db.Column(db.SmallInteger, nullable=False)
#     is_graduated = db.Column(db.SmallInteger, nullable=False)


#     def __init__(self, student_id, student_name, email, is_subscribed, is_graduated):
#         self.student_id = student_id
#         self.student_name = student_name
#         self.email = email
#         self.is_subscribed = is_subscribed
#         self.is_graduated = is_graduated


#     def json(self):
#         return {"student_id": self.student_id, "name": self.student_name, "email": self.email, "grad": self.is_graduated, "sub": self.is_subscribed}

# @app.route("/students/<string:student_id>/modules")
# def list_modules_by_id(student_id):
#     student = Student.query.filter_by(student_id=student_id).first()
#     if student:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": student.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "student_id": student_id
#             },
#             "message": "student not found."
#         }
#     ), 404

# @app.route("/")
# def home():
#     return "hello"

# if __name__ == '__main__':
#     app.run(port=5200, debug=True)

from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS

from student_models import db
from student_queries import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/module'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
CORS(app)


# We need to assign the resolvers to the corresponding fields in the Query and Mutation types
query = ObjectType("Query")
query.set_field("student", resolve_student)
query.set_field("students", resolve_students)
query.set_field("student_modules", resolve_student_modules)
mutation = ObjectType("Mutation")
mutation.set_field("create_student", resolve_create_student)
mutation.set_field("update_student", resolve_update_student)
mutation.set_field("delete_student", resolve_delete_student)
mutation.set_field("create_student_module", resolve_create_student_module)
mutation.set_field("update_student_module", resolve_update_student_module)
mutation.set_field("delete_student_module", resolve_delete_student_module)

type_defs = load_schema_from_path("student.graphql")
schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)


# We need to create a route for our GraphQL server
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

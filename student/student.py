from os import environ

from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS

from student_queries import *

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@host.docker.internal:3306/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
CORS(app, resources={r"/*": {"origins": "*"}})

# We need to assign the resolvers to the corresponding fields in the Query and Mutation types
query = ObjectType("Query")
query.set_field("get_student", resolve_student)
query.set_field("get_students", resolve_students)
query.set_field("get_student_module", resolve_student_module)
query.set_field("get_student_modules", resolve_student_modules)
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


@app.route('/student/<string:student_id>/modules')
def get_modules_by_student(student_id):
    modules = StudentModule.query.filter_by(student_id=student_id).all()
    if len(modules):
        return jsonify(
            {
                "code": 200,
                "data": [module.to_dict() for module in modules]
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "student_id": student_id
            },
            "message": "Student not found."
        }
    ), 404


@app.route('/students/subscription')
def get_students_by_subscription():
    students = Student.query.filter_by(is_subscribed=True).all()
    if len(students):
        return jsonify(
            {
                "code": 200,
                "data": [student.to_dict() for student in students]
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {},
            "message": "No students found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

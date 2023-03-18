from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS

from student_models import db
from student_queries import *

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/module'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/student'
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

if __name__ == '__main__':
    app.run(port=5200, debug=True)
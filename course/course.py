from os import environ

from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS

from course_queries import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
CORS(app, resources={r"/*": {"origins": "*"}})

# We need to assign the resolvers to the corresponding fields in the Query and Mutation types
query = ObjectType("Query")
query.set_field("get_course", resolve_course)
query.set_field("get_courses", resolve_courses)
query.set_field("get_course_skills", resolve_course_skills)
mutation = ObjectType("Mutation")
mutation.set_field("create_course", resolve_create_course)
mutation.set_field("update_course", resolve_update_course)
mutation.set_field("delete_course", resolve_delete_course)
mutation.set_field("create_course_skill", resolve_create_course_skill)
mutation.set_field("update_course_skill", resolve_update_course_skill)
mutation.set_field("delete_course_skill", resolve_delete_course_skill)

type_defs = load_schema_from_path("course.graphql")
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


@app.route('/courses')
def get_courses():
    courses = Course.query.all()
    if courses:
        return jsonify(
            {
                "code": 200,
                "data": [course.to_dict() for course in courses]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No courses found"
        }
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)

from os import environ

from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS

from module_queries import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
CORS(app, resources={r"/*": {"origins": "*"}})

# We need to assign the resolvers to the corresponding fields in the Query and Mutation types
query = ObjectType("Query")
query.set_field("get_module", resolve_module)
query.set_field("get_modules", resolve_modules)
query.set_field("get_module_skills", resolve_module_skills)
mutation = ObjectType("Mutation")
mutation.set_field("create_module", resolve_create_module)
mutation.set_field("update_module", resolve_update_module)
mutation.set_field("delete_module", resolve_delete_module)
mutation.set_field("create_module_skill", resolve_create_module_skill)
mutation.set_field("update_module_skill", resolve_update_module_skill)
mutation.set_field("delete_module_skill", resolve_delete_module_skill)

type_defs = load_schema_from_path("module.graphql")
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


@app.route('/module/<string:module_id>')
def get_module(module_id):
    module = Module.query.get(module_id)
    if module:
        return jsonify(
            {
                "code": 200,
                "data": module.to_dict()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "module_id": module_id
            },
            "message": "Module not found."
        }
    ), 404


@app.route('/modules')
def get_modules():
    modules = Module.query.all()
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
            "data": {},
            "message": "No modules found."
        }
    ), 404


@app.route('/module/<string:module_id>/skills')
def get_skills_by_module(module_id):
    skills = ModuleSkill.query.filter_by(module_id=module_id).all()
    if len(skills):
        return jsonify(
            {
                "code": 200,
                "data": [skill.to_dict() for skill in skills]
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "module_id": module_id
            },
            "message": "Module not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

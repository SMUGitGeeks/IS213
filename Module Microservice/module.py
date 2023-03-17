from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from module_queries import resolve_module, resolve_modules, resolve_module_skills, resolve_create_module, resolve_update_module, resolve_delete_module, resolve_create_module_skill, resolve_update_module_skill, resolve_delete_module_skill
from module_models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/module'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
CORS(app)


# We need to assign the resolvers to the corresponding fields in the Query and Mutation types
query = ObjectType("Query")
query.set_field("module", resolve_module)
query.set_field("modules", resolve_modules)
query.set_field("module_skills", resolve_module_skills)
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

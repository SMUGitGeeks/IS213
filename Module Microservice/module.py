from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from module_queries import resolve_module, resolve_module_skill

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/module'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
CORS(app)
db.create_all()


query = ObjectType("Query")
query.set_field("modules", resolve_module)
query.set_field("module_skills", resolve_module_skill)

type_defs = load_schema_from_path("module.graphql")
schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)

@app.route('/test', methods=['POST'])
def test_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

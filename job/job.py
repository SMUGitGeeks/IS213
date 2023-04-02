from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ

from job_models import db
from job_queries import resolve_job, resolve_jobs, resolve_job_skills, resolve_create_job, \
    resolve_update_job, resolve_delete_job, resolve_create_job_skill, resolve_update_job_skill, \
    resolve_delete_job_skill

app = Flask(__name__)
# using docker:
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# windows: app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/job'
# mac: app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/job'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()

CORS(app)


# We need to assign the resolvers to the corresponding fields in the Query and Mutation types
query = ObjectType("Query")
query.set_field("get_job", resolve_job)
query.set_field("get_jobs", resolve_jobs)
query.set_field("get_job_skills", resolve_job_skills)
mutation = ObjectType("Mutation")
mutation.set_field("create_job", resolve_create_job)
mutation.set_field("update_job", resolve_update_job)
mutation.set_field("delete_job", resolve_delete_job)
mutation.set_field("create_job_skill", resolve_create_job_skill)
mutation.set_field("update_job_skill", resolve_update_job_skill)
mutation.set_field("delete_job_skill", resolve_delete_job_skill)

type_defs = load_schema_from_path("job.graphql")
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
    status_code = 200
    # this part does not work
    return jsonify({"result": result, "code":status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
from os import environ

from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from flask import Flask, request, jsonify
from flask_cors import CORS

from job_queries import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
CORS(app, resources={r"/*": {"origins": "*"}})

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
    return jsonify({"result": result, "code": status_code})


@app.route('/jobs')
def get_jobs():
    jobs = Job.query.all()
    if len(jobs):
        return jsonify(
            {
                "code": 200,
                "data": [job.to_dict() for job in jobs]
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {},
            "message": "No jobs found."
        }
    ), 404


@app.route('/job/<string:job_id>')
def get_job(job_id):
    job = Job.query.get(job_id)
    if job:
        return jsonify(
            {
                "code": 200,
                "data": job.to_dict()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "job_id": job_id
            },
            "message": "Job not found."
        }
    ), 404


@app.route('/job/<string:job_id>/skills')
def get_skills_by_job(job_id):
    skills = JobSkill.query.filter_by(job_id=job_id).all()
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
                "job_id": job_id
            },
            "message": "Skills not found."
        }
    ), 404


@app.route('/job/<string:skill_name>/jobs')
def get_jobs_by_skill(skill_name):
    jobs = JobSkill.query.filter_by(skill_name=skill_name).all()
    # return [module.to_dict() for module in modules]
    if len(jobs):
        return jsonify(
            {
                "code": 200,
                "data": [job.to_dict() for job in jobs]
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "skill_name": skill_name
            },
            "message": "Jobs not found."
        }
    ), 404


@app.route('/job', methods=['POST'])
def create_job():
    job = Job(
        job_role=request.json['job_role'],
        job_description=request.json['job_description'],
        job_company=request.json['job_company'],
    )
    db.session.add(job)
    db.session.commit()
    if job:
        return jsonify(
            {
                "code": 201,
                "data": job.to_dict()
            }
        )
    return jsonify(
        {
            "code": 400,
            "data": {},
            "message": "Job not created."
        }
    ), 400


@app.route('/job/<string:job_id>', methods=['POST'])
def create_job_skill(job_id):
    job_skill = JobSkill(
        job_id=job_id,
        skill_name=request.json['skill_name'],
    )
    db.session.add(job_skill)
    db.session.commit()
    if job_skill:
        return jsonify(
            {
                "code": 201,
                "data": job_skill.to_dict()
            }
        )
    return jsonify(
        {
            "code": 400,
            "data": {},
            "message": "Job Skill not created."
        }
    ), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

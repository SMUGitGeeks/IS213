from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

from invokes import invoke_http

app = Flask(__name__)
CORS(app)
# all the URLs
student_URL = environ.get('student_URL') or "http://localhost:5001/graphql"
job_URL = environ.get('job_URL') or "http://localhost:5002/graphql"
module_URL = environ.get('module_URL') or "http://localhost:5000/graphql"
error_URL = ""

def apply_job(student_id, job_id):

    # 1. Get student's modules by graphql
    print('\n-----Invoking student microservice-----')
    student_modules_query = "query { get_student_modules(student_id: \"" + student_id + "\") { student_modules { module_id } success errors } }"
    data = {
        'query': student_modules_query 
    }
    student_modules_data = invoke_http(student_URL + 'graphql', method='POST', json=data)
    student_modules = student_modules_data['data']['get_student_modules']['student_modules']

    if not student_modules_data['data']['get_student_modules']['success']:
        return invoke_error_microservice(student_modules_data, "student")
    
    student_modules = student_modules_data['data']['get_student_modules']['student_modules']
    #print('student_modules: ', student_modules)

    student_modules_list = []
    for detail in student_modules:
        student_modules_list.append(detail['module_id'])
    print('student_modules: ' + str(student_modules_list))
    
    # 2. Get all module skills by graphql
    print('\n-----Invoking module microservice-----')
    skills_data = []
    for module_id in student_modules_list:
        module_query = "query { get_module_skills (module_id: \"" + module_id +"\") { module_skills { skill_name } success errors } }"
        data = {
            'query': module_query
        }
    module_skills_data = invoke_http(module_URL + 'graphql', method='POST', json=data)

    if not module_skills_data['data']['get_module_skills']['success']:
        return invoke_error_microservice(module_skills_data, "module")
    # create list of module skills    
    skills_data += module_skills_data['data']['get_module_skills']['module_skills']

    # 3. Get job skills by graphql
    print('\n-----Invoking job microservice-----')
    job_skills_query = "query { get_job_skills(job_id: \"" + job_id + "\") { job_skills { job_id skill_name } success errors } }"
    data = {
        'query': job_skills_query
    }
    job_skills_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
    job_skills = job_skills_data['data']['get_job_skills']['job_skills']

    if not job_skills_data['data']['get_job_skills']['success']:
        return invoke_error_microservice(job_skills_data, "job")

    # Create job skill list
    job_skills_list = []
    for detail in job_skills:
        job_skills_list.append(detail['skill_name'])
    print('job_skills: ' + str(job_skills_list))


    # 4. Compare student's modules with job skills
    # 5. Compare student's modules with module skills
    # 6. Return result
    return {
        "code": 200,
        "data": {
            "student_id": student_id,
            "job_id": job_id,
            "student_modules": student_modules,
            "job_skills": job_skills
        },
        "message": "Successfully applied for job."
    }

# ++++ USING REST API +++++
# get all jobs
jobs_result = invoke_http(job_URL + '/jobs', method='GET')
    if student_modules_data['code'] != 200:
        return invoke_error_microservice(student_modules_data, 'student')
    student_modules = student_modules_data['data']


def invoke_error_microservice(json, microservice):
    print(f"-----Invoking error microservice as {microservice} fails.-----")
    invoke_http(error_URL, method="POST", json=json)
    # - reply from the invocation is not used; 
    # continue even if this invocation fails
    print("Sent to the error microservice:", json)

    # 7. Return error
    return {
            "code": 500,
            "data": json,
            "message": f"{microservice} failed, sent for error handling."
        }
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

from invokes import invoke_http
import requests

app = Flask(__name__)
CORS(app)
# all the URLs
student_URL = environ.get('student_URL') or "http://localhost:5001/graphql"
job_URL = environ.get('job_URL') or "http://localhost:5002/graphql"
module_URL = environ.get('module_URL') or "http://localhost:5000/graphql"
course_URL = environ.get('course_URL') or "http://localhost:5003/graphql"
error_URL = ""


# dispaly all jobs via REST API
def display_all_jobs():
    print('\n-----Invoking job microservice-----')
    job_data = invoke_http(job_URL + '/jobs', method='GET')
    if job_data['code'] != 200:
        return invoke_error_microservice(job_data, 'job')
    job_list = job_data['data']
    return jsonify(job_list), 200

@app.route('/apply/<string:student_id>/<string:job_id>', methods=['GET'])
def apply_job(student_id, job_id):
    # 1. Get student's modules by graphql
    print('\n-----Invoking student microservice-----')
    student_modules_query = "query { get_student_modules(student_id: \"" + student_id + "\") { student_modules { module_id } success errors } }"
    data = {
        'query': student_modules_query 
    }
    student_modules_data = invoke_http(student_URL + 'graphql', method='POST', json=data)
    if not student_modules_data['data']['get_student_modules']['success']:
        return invoke_error_microservice(student_modules_data, "student")
    student_modules = student_modules_data['data']['get_student_modules']['student_modules']
    
    # Create list of student modules
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
        
        # Create list of module skills    
        skills_data += module_skills_data['data']['get_module_skills']['module_skills']

    # 3. Get job skills by graphql
    print('\n-----Invoking job microservice-----')
    job_skills_query = "query { get_job_skills(job_id: \"" + job_id + "\") { job_skills { job_id skill_name } success errors } }"
    data = {
        'query': job_skills_query
    }
    job_skills_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
    if not job_skills_data['data']['get_job_skills']['success']:
        return invoke_error_microservice(job_skills_data, "job")
    job_skills = job_skills_data['data']['get_job_skills']['job_skills']

    # Create job skill list
    job_skills_list = []
    for detail in job_skills:
        job_skills_list.append(detail['skill_name'])

    # 4. Compare student's modules with job skills
    have_skill = True
    lack_skills = []
    for skill in job_skills_list:
        if skill in skills_data:
            continue
        else:
            have_skill = False
            lack_skills.append(skill)
    
    # 5. If there is lack skill, get course_id to learn those skills
    if not have_skill:
        courses_data = []
        print('\n-----Invoking course microservice-----')
        for skill in lack_skills:
            course_query = "query { get_courses (skill_name: \"" + skill +"\") { courses { course_id course_name course_link} success errors } }"
            data = {
                'query': course_query
            }
            course_data = invoke_http(course_URL + 'graphql', method='POST', json=data)
            if not course_data['data']['get_courses']['success']:
                return invoke_error_microservice(course_data, "course")
            courses_data += course_data['data']['get_courses']['courses']

        # 6. Return courses to learn those skills plus T/F to continue with application
        return {
            "code": 200,
            "data": {
                "job_id": job_id,
                "lack_skills": lack_skills,
                "courses": courses_data
            },
            "message": False
        }

    # 6. If there is no lack skill, return success
    else:
        return {
            "code": 200,
            "data": {
                "job_id": job_id,
            },
            "message": True
        }

def invoke_error_microservice(json, microservice):
    print(f"-----Invoking error microservice as {microservice} fails.-----")
    invoke_http(error_URL, method="POST", json=json)
    # - reply from the invocation is not used; 
    # continue even if this invocation fails
    print("Sent to the error microservice:", json)

    return {
            "code": 500,
            "data": json,
            "message": f"{microservice} failed, sent for error handling."
        }

@app.route('/apply/<string:student_id>/<string:job_id>', methods=['POST'])

def apply_job(student_id, job_id, form):
    if form.validate_on_submit():
            # takes the resume
            file = form.file.data
            studentID = str(form.student_id.data)
            jobID = str(form.job_id.data)


            url = "https://content.dropboxapi.com/2/files/upload"

            payload = file
            path = "/" + studentID + "_" + jobID

            headers = {
            'Authorization': 'Bearer sl.BbrM4lMJ5eOKlenEzSawDGeDlr4ndX4BE7xbgkjgryQybbbYeFrPBucrguud4xGXVmYyiXbEn_s7GpCaQMgSLNquoE3c6wfYX2adegAsL8BAEF5umD17TC1RxHcLkdtwPDYrjSk',
            'Dropbox-API-Arg': '{"autorename":false,"mode":"add","mute":false,"path":"'+ path +'.pdf","strict_conflict":false}',
            'Content-Type': 'application/octet-stream'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return(response.text)
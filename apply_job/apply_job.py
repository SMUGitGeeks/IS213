import json
import os
import sys
from os import environ

import pika
from flask import Flask, jsonify
from flask_cors import CORS

import amqp_setup
from invokes import invoke_http

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

student_URL = environ.get('studentURL')
job_URL = environ.get('jobURL')
module_URL = environ.get('moduleURL')
course_URL = environ.get('courseURL')


@app.route('/apply/<string:student_id>/<string:job_id>', methods=['GET'])
def get_suitability(student_id, job_id):
    amqp_setup.check_setup()
    try:
        # 1. Get student's modules by graphql
        print("------------------------------------")
        print('\n-----Invoking student microservice-----')
        microservice = "student"
        student_modules_query = "query { get_student_modules(student_id:" + student_id + ") { student_modules { module_id } success errors } }"
        data = {
            'query': student_modules_query
        }
        student_modules_data = invoke_http(student_URL + 'graphql', method='POST', json=data)

        # Create list of student modules
        student_modules = student_modules_data['data']['get_student_modules']['student_modules']
        student_modules_list = []
        for detail in student_modules:
            student_modules_list.append(detail['module_id'])
        print('student_modules: ' + str(student_modules_list))

        # 2. Get all module skills by graphql
        print('\n-----Invoking module microservice-----')
        microservice = "module"
        skills_data = []
        for module_id in student_modules_list:
            module_query = "query { get_module_skills (module_id: \"" + module_id + "\") { module_skills { skill_name } success errors } }"
            data = {
                'query': module_query
            }
            module_skills_data = invoke_http(module_URL + 'graphql', method='POST', json=data)
            module_skills = module_skills_data['data']['get_module_skills']['module_skills']

            # Create list of module skills
            for skill in module_skills:
                skills_data.append(skill['skill_name'])
        print('Skills that student has: ' + str(skills_data))

        # 3. Get job skills by graphql
        print('\n-----Invoking job microservice-----')
        microservice = "job"
        job_skills_query = "query { get_job_skills(job_id:" + job_id + ") { job_skills { job_id skill_name } success errors } }"
        data = {
            'query': job_skills_query
        }
        job_skills_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
        job_skills = job_skills_data['result']['data']['get_job_skills']['job_skills']

        # Create job skill list
        job_skills_list = []
        for detail in job_skills:
            job_skills_list.append(detail['skill_name'])
        print('Skills that job requires: ' + str(job_skills_list))

        # 4. Compare student's modules with job skills
        have_skill = True
        lack_skills = []
        for skill in job_skills_list:
            if skill in skills_data:
                continue
            else:
                have_skill = False
                lack_skills.append(skill)
        print("\nStudent is lacking these skills:" + str(lack_skills))

        # 5. If there is lack skill, get course_id to learn those skills
        if not have_skill:
            # Check if student is graduated
            student_query = "query { get_student (student_id:" + student_id + ") { student { is_graduated } success errors } }"
            data = {
                'query': student_query
            }
            student_data = invoke_http(student_URL + 'graphql', method='POST', json=data)
            is_graduated = student_data['data']['get_student']['student']['is_graduated']

            # if student is not graduated, look for modules to learn those skills
            final_modules = []
            if is_graduated == 0:
                print("\nStudent is not graduated")
                print('-----Invoking module microservice-----')
                microservice = "module"
                modules_data = []
                for skill in lack_skills:
                    module_query = "query { get_modules (skill_name: \"" + skill + "\") { modules { module_id module_name} success errors } }"
                    data = {
                        'query': module_query
                    }
                    module_data = invoke_http(module_URL + 'graphql', method='POST', json=data)
                    modules_data += module_data['data']['get_modules']['modules']

                # Create list of unqiue modules that student has not taken but needed for the job
                for module in modules_data:
                    if (module not in final_modules):
                        final_modules.append(module)
                print('SMU Modules to learn those skills: ' + str(final_modules))

            # for all students, look for external courses to learn those skills
            courses_data = []
            final_courses = []
            print('\n-----Invoking course microservice-----')
            microservice = "course"
            for skill in lack_skills:
                course_query = "query { get_courses (skill_name: \"" + skill + "\") { courses { course_id course_name course_link} success errors } }"
                data = {
                    'query': course_query
                }
                course_data = invoke_http(course_URL + 'graphql', method='POST', json=data)
                courses_data += course_data['data']['get_courses']['courses']

            # Create list of unqiue courses
            for course in courses_data:
                if course not in final_courses:
                    final_courses.append(course)
            print('Courses to learn those skills: ' + str(final_courses))

            # 6. Return courses to learn those skills plus T/F to continue with application
            if final_modules == []:
                return {
                    "code": 200,
                    "data": {
                        "job_id": job_id,
                        "lack_skills": lack_skills,
                        "courses": final_courses
                    },
                    "message": False
                }

            return {
                "code": 200,
                "data": {
                    "job_id": job_id,
                    "lack_skills": lack_skills,
                    "courses": final_courses,
                    "modules": final_modules
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
    except Exception as e:
        # Unexpected error in code
        print(f"\n\n-----Invoking error microservice as {microservice} fails.-----")
        print(f"-----Publishing the error message with routing_key={microservice}.error-----")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        code = 500
        message = json.dumps({
            "code": code,
            "message": "apply_job.py internal error: " + ex_str
        })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"{microservice}.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 500,
            "message": "apply_job.py internal error: " + ex_str
        }), 500


# @app.route('/apply/<string:student_id>/<string:job_id>', methods=['POST'])
# def post_resume(student_id, job_id, resume):
#         amqp_setup.check_setup()
#         try:
#             # takes the resume
#             # return(resume)
#             file = resume
#             url = "https://content.dropboxapi.com/2/files/upload"

#             payload = file
#             path = "/" + student_id + "_" + job_id

#             headers = {
#                     'Authorization': 'Bearer sl.Bb-oDML-7CjIRkPNO7UEXnHqfrQs4oYNQAmnDM73F3arwDMaXcOWNmFT138tw_5RtEqugcpC6OPuH7uJbh7WcbbxzXEsMb10AspaOG2kO7QAPjDk1a-OxTmv41C1Yw5_J0tHsGI',
#                     'Dropbox-API-Arg': '{"autorename":false,"mode":"add","mute":false,"path":"'+ path +'.pdf","strict_conflict":false}',
#                     'Content-Type': 'application/octet-stream'
#                     }

#             response = requests.request("POST", url, headers=headers, data=payload)

#             return(response.text)

#         except Exception as e:
#             # Unexpected error in code
#             print(f"\n\n-----Invoking error microservice as resume uploading fails.-----")
#             print(f"-----Publishing the error message with routing_key=resume.error-----")
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
#             print(ex_str)

#             code = 500
#             message = json.dumps({
#                 "code": code,
#                 "message": "apply_job.py internal error: " + ex_str
#             })

#             amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"resume.error", 
#                 body=message, properties=pika.BasicProperties(delivery_mode = 2))

#             return json({
#                 "code": 500,
#                 "message": "apply_job.py internal error: " + ex_str
#             }), 500

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for applying a job...")
    app.run(host="0.0.0.0", port=5006, debug=True)

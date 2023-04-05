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


@app.route('/<string:student_id>')
def check_student(student_id):
    try:
        if student_id:
            print('\n-----Invoking student microservice-----')
            # Verify valid student_id ===============================
            if not student_id.isnumeric():
                return {
                    'code': 400,
                    'message': 'Invalid Student ID.'
                }
            student_query = "query { get_student (student_id:" + student_id + ") { student { student_id } success errors } }"
            data = {
                'query': student_query
            }
            student_data = invoke_http(student_URL + 'graphql', method='POST', json=data)
            print('student_id: ' + student_id)

        return jsonify({
            "code": 200,
            "data": student_data
        }), 200

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)


@app.route('/match/<string:student_id>')
def get_job(student_id):
    amqp_setup.check_setup()
    try:
        if student_id:
            # try:
            result = match(student_id)
            # return jsonify(result), result["code"]
            return result
    except Exception as e:
        # Unexpected error in code
        print(f"\n\n-----Invoking error microservice as job fails.-----")
        print(f"-----Publishing the error message with routing_key=job.error-----")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        code = 500
        message = json.dumps({
            "code": code,
            "message": "match_job.py internal error: " + ex_str
        })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"job.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 500,
            "message": "match_job.py internal error: " + ex_str
        }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid Student_ID input: " + str(student_id)
    }), 400


def match(student_id):
    amqp_setup.check_setup()
    try:
        print('\n-----Invoking student microservice-----')
        # Get Student Modules ==================================
        # ++++ USING GRAPHQL +++++
        student_modules_query = "query { get_student_modules (student_id: " + student_id + ") { student_modules { module_id } success errors } }"
        data = {
            'query': student_modules_query
        }
        student_modules_data = invoke_http(student_URL + 'graphql', method='POST', json=data)
        student_modules = student_modules_data['data']['get_student_modules']['student_modules']

        # ++++ USING REST API +++++
        # student_modules_result = invoke_http(student_URL + 'students/' + student_id + '/modules')
        # student_modules = student_modules_result['data']

        # Create list of modules
        student_modules_list = []
        for detail in student_modules:
            student_modules_list.append(detail['module_id'])
        print('student_modules: ' + str(student_modules_list))

    except Exception as e:
        print(f"\n\n-----Invoking error microservice as student fails.-----")
        print(f"-----Publishing the error message with routing_key=student.error-----")
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        code = 500
        message = json.dumps({
            "code": code,
            "message": "match_job.py internal error: " + ex_str
        })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"student.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 500,
            "message": "match_job.py internal error: " + ex_str
        }), 500

    try:
        print('\n-----Invoking module microservice-----')
        skills_data = []

        # Get all module skills
        for module_id in student_modules_list:
            module_query = "query { get_module_skills (module_id: \"" + module_id + "\") { module_skills { skill_name } success errors } }"
            data = {
                'query': module_query
            }
            module_skills_data = invoke_http(module_URL + 'graphql', method='POST', json=data)
            skills_data += module_skills_data['data']['get_module_skills']['module_skills']

        # Create list of student skills
        student_skills_list = []
        for detail in skills_data:
            skill = detail['skill_name']
            if skill not in student_skills_list:
                student_skills_list.append(skill)
        print('student_skills: ' + str(student_skills_list))

    except Exception as e:
        print(f"\n\n-----Invoking error microservice as module fails.-----")
        print(f"-----Publishing the error message with routing_key=module.error-----")
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        code = 500
        message = json.dumps({
            "code": code,
            "message": "match_job.py internal error: " + ex_str
        })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"module.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 500,
            "message": "match_job.py internal error: " + ex_str
        }), 500

    try:
        print('\n-----Invoking job microservice-----')

        # Get Jobs with skills ============
        # +++++++ USING GRAPHQL +++++++
        job_frequency_dict = {}
        for skill in student_skills_list:
            jobs_query = "query { get_jobs(skill_name: \"" + skill + "\") { jobs { job_id job_role job_description job_company } success errors } }"
            data = {
                'query': jobs_query
            }
            jobs_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
            jobs = jobs_data['result']['data']['get_jobs']['jobs']

            if jobs != []:
                for job_detail in jobs:
                    job_id = str(job_detail['job_id'])
                    print('job_id: ' + job_id)

                    if job_id in job_frequency_dict:
                        job_frequency_dict[job_id]['freq'] += 1
                    else:
                        job_frequency_dict[job_id] = {'freq': 1, 'data': job_detail}

        # ++++++ USING REST API ++++++
        # for skill in student_skills_list:
        #     jobs_result = invoke_http(job_URL + 'job/' + skill + '/jobs')
        #     if jobs_result['code'] == 200:
        #         for job_skill_detail in jobs_result['data']:
        #             job_id = job_skill_detail['job_id']
        #             print('job_id: ' + job_id)

        #             job_detail_result = invoke_http(job_URL + 'job/' + job_id)
        #             if job_id in job_frequency_dict:
        #                 job_frequency_dict[job_id]['freq'] += 1
        #             else:
        #                 job_frequency_dict[job_id] = {'freq': 1, 'data': job_detail_result}

        # Return if no jobs ==================
        if job_frequency_dict == {}:
            return {
                "code": 200,
                "message": "No jobs found"
            }

        # Arrange Job by frequency ==========
        sorted_job_tuple_list = sorted(job_frequency_dict.items(), key=lambda x: x[1]['freq'], reverse=True)

        sorted_jobs_list = []
        for a_tuple in sorted_job_tuple_list:
            print(a_tuple)
            # sorted_jobs_list.append(a_tuple[1]['data']['data'])
            sorted_jobs_list.append(a_tuple[1]['data'])

        return {
            "code": 200,
            "data": sorted_jobs_list
        }

    except Exception as e:
        print(f"\n\n-----Invoking error microservice as job fails.-----")
        print(f"-----Publishing the error message with routing_key=job.error-----")
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        code = 500
        message = json.dumps({
            "code": code,
            "message": "match_job.py internal error: " + ex_str
        })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"job.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 500,
            "message": "match_job.py internal error: " + ex_str
        }), 500


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for matching a job...")
    app.run(host="0.0.0.0", port=5005, debug=True)

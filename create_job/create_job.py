import json
import os
import sys
from os import environ

import pika
from flask import Flask, request, jsonify
from flask_cors import CORS

import amqp_setup  # IMPORTANT -> Add this later
from invokes import invoke_http
from new_jobs_storage import NewJobs

app = Flask(__name__)
CORS(app)

student_URL = environ.get('studentURL')
job_URL = environ.get('jobURL')
email_URL = environ.get('emailURL')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Create Job Microservice Steps
#   -> Job Creation
#       -> Get new job from UI 
#       -> send creation request to job microservice 
#       -> receive status 
#       -> save job record (if success) 
#       -> return status to UI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ====================== Get Jobs from UI ======================
@app.route("/create_job", methods=['POST'])
def create_job():
    amqp_setup.check_setup()
    if request.is_json:
        try:
            newjob_record = request.get_json()
            print("\nReceived new job record in JSON:", newjob_record)
            # (COMMENT)
            # newjob_record should have both details of jobs and skills.
            # Example is used:
            # {
            # "job_role": "taxi driver",
            # "job_company": "grab",
            # "job_description": "vroom vroom",
            # "jobskills": ["python", "math knowledge", "driving skills"]
            # }

            result = add_job(newjob_record)
            # -> send new job to job microservice
            # -> receive status

            print('\n------------------------')
            print('returned')
            print(result)
            return (result)
            # print('\nresult: ', result)
            # return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            print(f"\n\n-----Invoking error microservice as create_job fails.-----")
            print("-----Publishing the error message with routing_key= create_job.error-----")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            code = 500
            message = json.dumps({
                "code": code,
                "message": "create_job.py internal error: " + ex_str
            })

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="create_job.error",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

            return jsonify({
                "code": 500,
                "message": "create_job.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    else:
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400


def add_job(record):
    # -> send new job to job microservice 
    # -> receive status 
    amqp_setup.check_setup()
    print('\n------------ Invoking job microservice ------------')

    # ====================== add new job record ======================

    job_role = record['job_role']
    job_description = record['job_description']
    job_company = record['job_company']
    api_key = record['api_key']

    job_mutation = "mutation{ create_job(job_role:\"" + job_role + "\", job_description: \"" + job_description + "\", job_company:\"" + job_company + "\"){ job{ job_id } success errors }}"

    data = {
        'query': job_mutation
    }

    headers = {
        'api-key': api_key
    }

    print('\n-----Adding new job record in job database-----')

    try:
        job_data = invoke_http(job_URL + 'graphql', headers=headers, method='POST', json=data)
        print(job_data)
        print(f"job successfully added")
        job_id = job_data['result']['data']['create_job']['job']['job_id']
        print(job_id)

    except Exception as e:
        print(f"\n\n-----Invoking error microservice as create_job fails.-----")
        print(f"-----Publishing the error message with routing_key=create_job.error-----")
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        code = 500
        message = json.dumps({
            "code": code,
            "message": "create_job.py internal error: " + ex_str
        })

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"create_job.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 500,
            "message": "create_job.py internal error: " + ex_str
        }), 500

    # ====================== Add new job skill ======================

    jobskills = record['jobskills']

    for jobskill in jobskills:

        # print(jobskill)

        jobskill_mutation = "mutation{ create_job_skill(job_id:" + str(
            job_id) + ", skill_name:\"" + jobskill + "\"){ success errors }}"

        data = {
            'query': jobskill_mutation
        }
        print('\n-----Adding new job skill in job skill database-----')

        try:
            jobskill_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
            print(jobskill_data)

        except Exception as e:
            print(f"\n\n-----Invoking error microservice as create job_skill fails.-----")
            print(f"-----Publishing the error message with routing_key=job_skill.error-----")
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            code = 500
            message = json.dumps({
                "code": code,
                "message": "create_job.py internal error: " + ex_str
            })

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=f"job_skill.error",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

            return jsonify({
                "code": 500,
                "message": "create_job.py internal error: " + ex_str
            }), 500

    print("\n")
    print('Adding job record into new_jobs_storage')
    new_jobs = NewJobs()

    # Add a job to the job list 
    new_jobs._job_dict[job_id] = {"job role": job_role, "job description": job_description, "job company": job_company}

    print("\n")
    print("------------------------------")
    print('Getting data from new_jobs_storage')

    job_dict = new_jobs.job_dict
    print(job_dict)
    print("------------------------------")
    return jsonify({
        "code": 200,
        "message": "Job added"
    }), 200
    # =================================================================


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Send Data to Email Microservice Steps
#    -> Create time based function
#    -> Student Email Retrieval
#    -> Get job dictionary from new_jobs_storage
#    -> Send data to email microservice
#    -> Clear job dictionary in new_jobs_storage 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/send_email", methods=['POST'])
def send_to_email():
    amqp_setup.check_setup()
    print('\n------------ Invoking student microservice ------------')
    # ====================== Get list of emails ======================
    email_query = """
    query {
        get_students {
            students {
                student_name
                email
                is_subscribed
            }
            success
            errors
        }
    }
    """

    data = {
        'query': email_query
    }

    sub_emails = invoke_http(student_URL + 'graphql', method='POST', json=data)

    print('------------------------######')
    print(sub_emails)
    print('------------------------######')

    students = sub_emails['data']['get_students']['students']

    # get students only who is subscribed
    subscribed_students = [student['email'] for student in students if student['is_subscribed']]
    # subscribed_students = ['glenlow12374@gmail.com', 'dx19999@hotmail.com', 'ssy.darryl@gmail.com']

    print(subscribed_students)

    new_jobs = NewJobs()
    jobs = new_jobs.job_dict

    print('new_jobs to send to email:')
    print(jobs)

    message1 = {"subscribed_students": subscribed_students, "new_jobs": jobs}
    print('\ntest100')
    print(message1)

    message = json.dumps(message1)
    print('\ntest2')
    print(message)

    new_jobs.clear_list()

    amqp_setup.check_setup()
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="send.notify", body=message,
                                     properties=pika.BasicProperties(delivery_mode=2))


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5007, debug=True)

## new python file

# class objectname(){
#         constructor..
#             jobs = []

#         addingjob(job):
#             jobs.append(job)

#         publishdata():
#             subscribers = student/graphql
#             amqp.send([jobs, subscribers])
# }

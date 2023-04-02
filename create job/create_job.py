from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

from new_jobs_storage import NewJobs

# import amqp_setup         # IMPORTANT -> Add this later
import pika
import json

app = Flask(__name__)
CORS(app)


student_URL = "http://localhost:5001/"
job_URL = "http://localhost:5002/"
email_URL = "http://localhost:5008/"
#error_URL = "http://localhost:5004/"


# Create Job Microservice Steps
#   -> Job Creation
#       -> Get new job from UI 
#       -> send creation request to job microservice 
#       -> receive status 
#       -> save job record (if success) 
#       -> return status to UI


 # ====================== Get Jobs from UI ======================
@app.route("/create_job", methods=['POST'])
def create_job():

    if request.is_json:
        try:
            newjob_record = request.get_json()
            print("\nReceived new job record in JSON:", newjob_record)
                # (COMMENT)
                # newjob_record should have both details of jobs and skills.
                # Example is used:
                # {
                    # "job_id": 200,
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
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            
            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
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


    print('\n############## Invoking job microservice ##############')

    # ====================== add new job record ======================

    job_id = record['job_id']
    job_role = record['job_role']
    job_description = record['job_description']
    job_company = record['job_company']

    job_mutation = "mutation{ create_job(job_id:\"" +str(job_id)+ "\",    job_role:\"" +job_role+ "\", job_description: \"" +job_description+ "\", job_company:\"" +str(job_id)+ "\"){ success errors }}"

    data = {
            'query': job_mutation
            }

    print('\n-----Adding new job record in job database-----')

    try: 
        job_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
        # print(job_data)

        # ADD ERROR CODE HERE
        if job_data['code'] in range(200,300):
            if job_data['result']['data']['create_job']['errors']:
        
                print('\n')
                print(f"Failed to add job with job_id: {job_id}")
                print('\n')
                
                result =  invoke_error_microservice(job_data, "job")

                return result
            
            else:
                    print(f"job with job_id: {job_id} successfully added")

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "Failed to invoke job microservice"
        }), 500
    

    # ====================== Add new job skill ======================

    jobskills = record['jobskills']

    for jobskill in jobskills:

        # print(jobskill)

        jobskill_mutation = "mutation{ create_job_skill(job_id:\"" + str(job_id) + "\", skill_name:\"" + jobskill + "\"){ success errors }}"

        data = {
            'query': jobskill_mutation
        }
        print('\n-----Adding new job skill in job skill database-----')

        try: 
            jobskill_data = invoke_http(job_URL + 'graphql', method='POST', json=data)

            # print(jobskill_data)
           
            if jobskill_data['code'] in range(200,300):
                if jobskill_data['result']['data']['create_job_skill']['errors']:
            
                    
                    print(f"Failed to add job skill {jobskill}")
                    print('\n')
                    
                    result =  invoke_error_microservice(jobskill_data, "jobskill")

                    return result
                
                else:
                    print(f"job skill {jobskill} successfully added")

        except Exception as e:
        # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Failed to add job record"
            }), 500
        


    print("\n")
    print('Adding job record into new_jobs_storage')
    new_jobs = NewJobs()

    # Add a job to the job list
    new_jobs._job_dict[job_id]= {"job role": job_role, "job description": job_description, "job company": job_company}

    print("\n")
    print("####################################")
    print('Getting data from new_jobs_storage')

    job_dict = new_jobs.job_dict
    print(job_dict)
    print("####################################")




    return jsonify({
                "code": 200,
                "message": "Job added"
            }), 200
    # =================================================================




def invoke_error_microservice(json, microservice):
    print(f'\n\n############## Invoking error microservice as {microservice} fails ##############')
    #### invoke_http(error_URL, method="POST", json=json)
    # - reply from the invocation is not used; 
    # continue even if this invocation fails
    # can change to amqp
    print("Sent to the error microservice:", json)

    # 7. Return error
    return jsonify({
            "code": 500,
            "message": f"{microservice} failed, sent for error handling."
        }),500



    


# while True():
#     objectname.publish_data()
#     time.sleep(1 week)



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)



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
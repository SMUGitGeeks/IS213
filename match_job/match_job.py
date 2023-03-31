from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

from invokes import invoke_http

app = Flask(__name__)
CORS(app)

student_URL = "http://localhost:5001/graphql"
job_URL = "http://localhost:5002/graphql"
module_URL = "http://localhost:5000/graphql"
error_URL = ""

@app.route('/jobs/<string:job_id>')
def get_job(job_id):
    if job_id:
        try:
            result = match(job_id)
            return jsonify(result), result["code"]
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
        
    return jsonify({
        "code": 400,
        "message": "Invalid JobID input: " + str(request)
    }), 400


def match(job_id):
    print('\n-----Invoking job microservice-----')
    job_skills_query = """"
        query {
            get_job_skills (job_id: {}) {
                job_skills {
                    job_id
                    skill_name
                }
            }
        }
    """.format(job_id)
    job_skills = invoke_http(job_URL, method='POST', json=job_skills_query.get_json())
    print('job_skills:', job_skills)

    # if not job_skills['success']:
    #     return invoke_error_microservice(job_skills, "job")
    
    # job_query = """"
    #     query {
    #         get_job (job_id: ${job_id}) {
    #             job {
    #                 job_id
    #                 job_role
    #                 job_description
    #                 job_company
    #             }
    #         }
    #     }
    # """
    # job = invoke_http(job_URL, method='POST', json=job_query)
    # print('job:', job)

    # if job['success']:
    #     return invoke_error_microservice(job, "job")


    # print('\n-----Invoking student microservice-----')
    # student_query = """"
    #     query {
    #         get_student_modules (student_id: {student_id}) {
    #             student_modules {
    #                 module_id
    #             }
    #         }
    #     }
    # """
    # student_modules = invoke_http(student_URL, method='POST', json=student_query)
    # print('student_modules:', student_modules)

    # if student_modules['success']:
    #     return invoke_error_microservice(student_modules, "student")


    # print('\n-----Invoking module microservice-----')
    # modules_skills_list =[]
    # for module_id in student_modules:
    #     module_query = """"
    #         query {
    #             get_module_skills (module_id: {module_id}) {
    #                 module_skills {
    #                     skill_name
    #                 }
    #             }
    #         }
    #     """.get_json()
    #     module_skills = invoke_http(module_URL, method='POST', json=module_query)

    #     if module_skills['success']:
    #         return invoke_error_microservice(module_skills, "module")


    #     # Append each skill into list
    #     modules_skills_list += module_skills
    # print('modules_skills_list:', modules_skills_list)




    # # ==========================================
    # # Below will be validation / matching codes
    # # ==========================================

    # # Supposing all are already lists
    # total_match = 0
    # for job_skill in job_skills:
    #     for module_skill in modules_skills_list:
    #         if job_skill == module_skill:
    #             total_match += 1
    
    
    # match_percentage = (total_match / len(job_skills)) * 100

    # return {
    #     "code": 200,
    #     "match_percentage": "{match_percentage:2d}%",
    #     "data": job
    # }

def invoke_error_microservice(json, microservice):
    print('\n\n-----Invoking error microservice as order fails-----')
    invoke_http(error_URL, method="POST", json=json)
    # - reply from the invocation is not used; 
    # continue even if this invocation fails
    print("Order status ({:d}) sent to the error microservice:", json)

    # 7. Return error
    return {
            "code": 500,
            "data": {"${microservice}_result": json},
            "message": "${microservice} failed, sent for error handling."
        }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for matching a job...")
    app.run(host="0.0.0.0", port=5005, debug=True)
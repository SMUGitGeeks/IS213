from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

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


# -> Get new job from UI 

@app.route("/create_job", methods=['POST'])
def create_job():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            newjob_record = request.get_json()
            print("\nReceived new job record in JSON:", newjob_record)

            # newjob_record should have both details of jobs and skills.
            # {{'job': jobs_details},
            # {'jobskills': jobskills_details }}



           # -> send new job to job microservice 
           # -> receive status 

            result = add_job(newjob_record)


            print('\n------------------------')
            print('\nresult: ', result)
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

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



    # -> send new job to job microservice 
    # -> receive status 

def add_job(record):

    print('\n-----Invoking job microservice-----')

    # ====================== add new job record ======================
    job_id = record['job_id']
    job_role = record['job_role']
    job_description = record['job_description']
    job_company = record['job_company']

    job_mutation = "mutation{ create_job(job_id:\"" +str(job_id)+ "\",    job_role:\"" +job_role+ "\", job_description: \"" +job_description+ "\", job_company:\"" +str(job_id)+ "\"){ success errors }}"

    data = {
        'query': job_mutation
    }

    print('\n-----Adding new job record in database-----')
    try: 
        
        job_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
        print("======TEST 1======")
        print(job_data)
        print("======TEST 2======")
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
    
    # =================================================================

    # if job_data['code'] not in range


    # add jobskills ===============
    jobskills = record['jobskills']

    for jobskill in jobskills:

        jobskill_mutation = "mutation{ create_job_skill('job_id':" + str(job_id) + ", 'skill_name':" + jobskill + "){ success errors }}"

        data = {
            'mutation': jobskill_mutation
        }

        try: 
            jobskill_data = invoke_http(job_URL + 'graphql', method='POST', json=data)
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








    

#     # invoke error microservice ===============
#     # !!!!!!!!!!!!!RELOOK AGAIN!!!!!!!!!!!!!!!!!
#     if not jobskill_data['data']['create_job_skill']['success']:
#         return invoke_error_microservice(job_mutation, "job")
#     print('job_id: ' + job_id)

#     # =============================================

#     # create_job(job_id: String!, job_role: String!, job_description: String!, job_company: String!): JobResult!

#     # create_job_skill(job_id: String!, skill_name: String!): JobSkillResult!


    
#     order_result = invoke_http(order_URL, method='POST', json=order)
#     print('order_result:', order_result)
  

#     # Check the order result; if a failure, send it to the error microservice.
#     code = order_result["code"]
#     message = json.dumps(order_result)

#     if code not in range(200, 300):
#         # Inform the error microservice
#         #print('\n\n-----Invoking error microservice as order fails-----')
#         print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

#         # invoke_http(error_URL, method="POST", json=order_result)
#         amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
#         # make message persistent within the matching queues until it is received by some receiver 
#         # (the matching queues have to exist and be durable and bound to the exchange)

#         # - reply from the invocation is not used;
#         # continue even if this invocation fails        
#         print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
#             code), order_result)

#         # 7. Return error
#         return {
#             "code": 500,
#             "data": {"order_result": order_result},
#             "message": "Order creation failure sent for error handling."
#         }

#     # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
#     # In http version, we first invoked "Activity Log" and then checked for error.
#     # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
#     # and a message sent to “Error” queue can be received by “Activity Log” too.

#     else:
#         # 4. Record new order
#         # record the activity log anyway
#         #print('\n\n-----Invoking activity_log microservice-----')
#         print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')        

#         # invoke_http(activity_log_URL, method="POST", json=order_result)            
#         amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
#             body=message)
    
#     print("\nOrder published to RabbitMQ Exchange.\n")
#     # - reply from the invocation is not used;
#     # continue even if this invocation fails
    
#     # 5. Send new order to shipping
#     # Invoke the shipping record microservice
#     print('\n\n-----Invoking shipping_record microservice-----')    
    
#     shipping_result = invoke_http(
#         shipping_record_URL, method="POST", json=order_result['data'])
#     print("shipping_result:", shipping_result, '\n')

#     # Check the shipping result;
#     # if a failure, send it to the error microservice.
#     code = shipping_result["code"]
#     if code not in range(200, 300):
#         # Inform the error microservice
#         #print('\n\n-----Invoking error microservice as shipping fails-----')
#         print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

#         # invoke_http(error_URL, method="POST", json=shipping_result)
#         message = json.dumps(shipping_result)
#         amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2))

#         print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
#             code), shipping_result)

#         # 7. Return error
#         return {
#             "code": 400,
#             "data": {
#                 "order_result": order_result,
#                 "shipping_result": shipping_result
#             },
#             "message": "Simulated shipping record error sent for error handling."
#         }

#     # 7. Return created order, shipping record
#     return {
#         "code": 201,
#         "data": {
#             "order_result": order_result,
#             "shipping_result": shipping_result
#         }
#     }








# ###############################################################################################



# @app.route('/graphql', methods=['POST'])
# def graphql_server():
#     data = request.get_json()
#     success, result = graphql_sync(
#         schema,
#         data,
#         context_value=request,
#         debug=app.debug
#     )
#     status_code = 200 if success else 400
#     return jsonify(result), status_code

# @app.route("/post_job", methods=['POST'])
# def receive_new_jobs(): #initially was place_order
#     # Simple check of input format and data of the request are JSON
#     # 3. Receive new updated jobs
#     if request.is_json:
#         try:
#             new_jobs = request.get_json()
#             # call student.py api
#             # emails = student.request.get_json()

#             objectname.addjob(job)


#             # 4. and 5. Get list of emails from student microservice {Email}
#             # response = requests.get(student_URL)

#             # if response.status_code == 200:
#             #     # Request successful, parse the response
#             #     print("----- Receiving emails from student -----")
#             #     emails = response.json()
#             #     print(emails)
#             # else:
#             #     # Request failed, handle the error
#             #     print('Error: ' + response.text)

            
#             # send a AMQP to emails microservice



#             emails = retrieve_student_email(new_jobs)
#             print('\n------------------------')
#             print('\nresult: ', result)
#             return jsonify(result), result["code"]

#         except Exception as e:
#             # Unexpected error in code
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
#             print(ex_str)

#             return jsonify({
#                 "code": 500,
#                 "message": "place_order.py internal error: " + ex_str
#             }), 500

#     # if reached here, not a JSON request.
#     return jsonify({
#         "code": 400,
#         "message": "Invalid JSON input: " + str(request.get_data())
#     }), 400


# def retrieve_student_email():
    
#     # 4 and 5.. Retrieve a list of emails of subscribed students from student microservice {Email}
#     # Invoke the student microservice
#     print('\n-----Invoking student microservice-----')
#     email_list = invoke_http(student_URL, method='GET')
#     print('email_list:', email_list)
  

#     # Check the email list; if a failure, send it to the error microservice.
#     code = email_list["code"]
#     message = json.dumps(email_list)

#     if code not in range(200, 300):
#         # Inform the error microservice
#         print('\n\n-----Publishing the (email error) message with routing_key= student.error-----')
#         amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="student.error", 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
#         # make message persistent within the matching queues until it is received by some receiver 
#         # (the matching queues have to exist and be durable and bound to the exchange)

#         # - reply from the invocation is not used;
#         # continue even if this invocation fails        
#         print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
#             code), email_list)

#         # 7. Return error
#         return {
#             "code": 500,
#             "data": {"email_list": email_list},
#             "message": "Email list retrieval failure sent for error handling."
#         }

#     # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
#     # In http version, we first invoked "Activity Log" and then checked for error.
#     # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
#     # and a message sent to “Error” queue can be received by “Activity Log” too.

   
#     # 6. Send list of emails and list of new jobs to email microservice
#     # Invoke the email microservice
#     print('\n\n-----Invoking email microservice-----')    
    
#     email_result = invoke_http(
#         email_URL, method="POST", json=email_list)
#     print("shipping_result:", shipping_result, '\n')

#     # Check the shipping result;
#     # if a failure, send it to the error microservice.
#     code = shipping_result["code"]
#     if code not in range(200, 300):
#         # Inform the error microservice
#         #print('\n\n-----Invoking error microservice as shipping fails-----')
#         print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

#         # invoke_http(error_URL, method="POST", json=shipping_result)
#         message = json.dumps(shipping_result)
#         amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2))

#         print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
#             code), shipping_result)

#         # 7. Return error
#         return {
#             "code": 400,
#             "data": {
#                 "order_result": order_result,
#                 "shipping_result": shipping_result
#             },
#             "message": "Simulated shipping record error sent for error handling."
#         }

    # 7. Return created order, shipping record
    return {
        "code": 200,
        "message": "successful"
        # "data": {
        #     "order_result": order_result,
        #     "shipping_result": shipping_result
        # }
    }


# while True():
#     objectname.publish_data()
#     time.sleep(1 week)



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.



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
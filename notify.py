from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

############################ ignore this ############################
#                                                                   #
#    #book_URL = "http://localhost:5000/book"                       #
#     order_URL = "http://localhost:5001/order"                     #
#     shipping_record_URL = "http://localhost:5002/shipping_record" #
#     activity_log_URL = "http://localhost:5003/activity_log"       #
#    #error_URL = "http://localhost:5004/error"                     #
#                                                                   #
#####################################################################


student_URL = "http://localhost:6001/student"
jobs_URL = "http://localhost:6002/jobs"
email_URL = "http://localhost:6008/email"
#error_URL = "http://localhost:5004/error"

# student 6001
# jobs 6002
# email 6008
# error tbc

# Get updated job/jobs

@app.route("/post_jobs", methods=['POST'])
def receive_new_jobs(): #initially was place_order
    # Simple check of input format and data of the request are JSON
    # 3. Receive new updated jobs
    if request.is_json:
        try:
            new_jobs = request.get_json()
            print("\nReceived an email in JSON:", new_jobs)

            # 4. and 5. Get list of emails from student microservice {Email}
            # response = requests.get(student_URL)

            # if response.status_code == 200:
            #     # Request successful, parse the response
            #     print("----- Receiving emails from student -----")
            #     emails = response.json()
            #     print(emails)
            # else:
            #     # Request failed, handle the error
            #     print('Error: ' + response.text)

            
            # send a AMQP to emails microservice



            emails = retrieve_student_email(new_jobs)
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


def retrieve_student_email():
    
    # 4 and 5.. Retrieve a list of emails of subscribed students from student microservice {Email}
    # Invoke the student microservice
    print('\n-----Invoking student microservice-----')
    email_list = invoke_http(student_URL, method='GET')
    print('email_list:', email_list)
  

    # Check the email list; if a failure, send it to the error microservice.
    code = email_list["code"]
    message = json.dumps(email_list)

    if code not in range(200, 300):
        # Inform the error microservice
        print('\n\n-----Publishing the (email error) message with routing_key= student.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="student.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), email_list)

        # 7. Return error
        return {
            "code": 500,
            "data": {"email_list": email_list},
            "message": "Email list retrieval failure sent for error handling."
        }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

   
    # 6. Send list of emails and list of new jobs to email microservice
    # Invoke the email microservice
    print('\n\n-----Invoking email microservice-----')    
    
    email_result = invoke_http(
        email_URL, method="POST", json=email_list)
    print("shipping_result:", shipping_result, '\n')

    # Check the shipping result;
    # if a failure, send it to the error microservice.
    code = shipping_result["code"]
    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as shipping fails-----')
        print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

        # invoke_http(error_URL, method="POST", json=shipping_result)
        message = json.dumps(shipping_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
            code), shipping_result)

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "shipping_result": shipping_result
            },
            "message": "Simulated shipping record error sent for error handling."
        }

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "shipping_result": shipping_result
        }
    }


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

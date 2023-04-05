# receives list of email and list of new jobs from notify microservice
# send job application update to list of students through email and twilio send grid

# !/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
from os import environ

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import amqp_setup

monitorBindingKey = '*.notify'


def receiveEmailInfo():
    amqp_setup.check_setup()

    queue_name = 'Email'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()  # an implicit loop waiting to receive messages;
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# callback here is point where email receives data through AMQP. Finish notify.py to know what is the data received.

def callback(channel, method, properties, body):  # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processEmailInfo(json.loads(body))
    print()  # print a new line feed


def processEmailInfo(email_info):
    print("Recording an email log:")
    print(email_info)
    email_list = email_info["subscribed_students"]
    print('#######################################')
    print(email_list)
    print('#######################################')
    new_jobs_dict = email_info["new_jobs"]
    email_string = '<table border="1"><tr><th>Job ID</th><th>Job Role</th><th>Job Description</th><th>Job Company</th></tr>'
    for key in new_jobs_dict:
        new_job_id = key
        new_job_info_dict = new_jobs_dict[key]
        new_job_role = new_job_info_dict["job role"]
        new_job_description = new_job_info_dict["job description"]
        new_job_company = new_job_info_dict["job company"]
        email_string += '<tr><th>' + new_job_id + '</th><td>' + new_job_role + '</td><td>' + new_job_description + '</td><td>' + new_job_company + '</td></tr>'
    email_string += '</table>'
    send_email(email_list, email_string)


def send_email(email_list, email_string):
    message = Mail(
        from_email='glen.low.2021@scis.smu.edu.sg',
        to_emails=email_list,
        subject='New Jobs This Month!',
        html_content=email_string
    )

    sg = SendGridAPIClient(environ.get('sendgridAPIKey'))
    response = sg.send(message)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveEmailInfo()

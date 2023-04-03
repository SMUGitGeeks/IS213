# receives list of email and list of new jobs from notify microservice
# send job application update to list of students through email and twilio send grid

#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import amqp_setup

monitorBindingKey='*.notify'

def receiveEmailInfo():
    amqp_setup.check_setup()
        
    queue_name = 'Email'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

# callback here is point where email receives data through AMQP. Finish notify.py to know what is the data received.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processEmailInfo(json.loads(body))
    print() # print a new line feed


def processEmailInfo(email_info):
    print("Recording an order log:")
    print(email_info)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveEmailInfo()

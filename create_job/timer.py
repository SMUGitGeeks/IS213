from invokes import invoke_http
import time
from os import environ

while True:

    create_job_URL = environ.get('createJobURL')
    invoke_http(create_job_URL + 'send_email', method='POST')
    time.sleep(30)
from invokes import invoke_http
import time

while True:

    createjob_URL = "http://localhost:5100/"
    invoke_http(createjob_URL + 'send_email', method='POST')
    time.sleep(60)
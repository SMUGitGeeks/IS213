FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
<<<<<<< HEAD:create_job/create_job.Dockerfile
COPY ./create_job.py ./invokes.py ./new_jobs_storage.py ./timer.py ./amqp_setup.py ./
CMD [ "python", "create_job.py" ]
CMD [ "python", "timer.py" ]
=======
COPY create_job/create_job.py create_job/invokes.py create_job/new_jobs_storage.py create_job/timer.py create_job/amqp_setup.py ./
CMD [ "python", "create_job.py" ]
>>>>>>> feature-match_job:create_job.Dockerfile

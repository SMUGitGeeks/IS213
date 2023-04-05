FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./create_job.py ./invokes.py ./new_jobs_storage.py ./timer.py ./amqp_setup.py ./
CMD [ "python", "create_job.py" ] && [ "python", "timer.py" ]
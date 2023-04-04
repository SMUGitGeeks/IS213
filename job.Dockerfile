FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY job/job.py .
COPY job/job_models.py .
COPY job/job_queries.py .
COPY job/job.graphql .
CMD [ "python", "./job.py" ]

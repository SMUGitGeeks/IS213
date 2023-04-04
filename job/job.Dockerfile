FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY job.py .
COPY job_models.py .
COPY job_queries.py .
COPY job.graphql .
CMD [ "python", "./job.py" ]

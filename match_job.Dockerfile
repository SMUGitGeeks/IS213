FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY match_job/match_job.py ./
COPY match_job/invokes.py ./
COPY apply_job/amqp_setup.py ./
CMD [ "python", "match_job.py" ]
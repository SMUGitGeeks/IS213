FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY apply_job.py ./
COPY invokes.py ./
CMD [ "python", "apply_job.py" ]
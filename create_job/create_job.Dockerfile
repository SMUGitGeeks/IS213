FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY create_job.py ./ invokes.py ./ new_jobs_storage.py ./ timer.py ./
CMD [ "python", "create_job.py" ]
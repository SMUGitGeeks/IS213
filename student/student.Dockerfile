FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY student_models.py .
COPY student_queries.py .
COPY student.graphql .
COPY student.py .
CMD [ "python", "student.py" ]
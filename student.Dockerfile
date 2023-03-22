FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY student/student.graphql .
COPY student/student.py .
COPY student/student_models.py .
COPY student/student_queries.py .
CMD [ "python", "student.py" ]
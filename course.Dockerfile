FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY course/course.py course/course.graphql course/course_models.py course/course_queries.py  ./
CMD [ "python", "./course.py" ]

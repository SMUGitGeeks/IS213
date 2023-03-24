FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY module.py .
COPY module_models.py .
COPY module_queries.py .
COPY module.graphql .
CMD [ "python", "./module.py" ]

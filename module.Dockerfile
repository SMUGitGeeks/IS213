FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY module/module.py .
COPY module/module_models.py .
COPY module/module_queries.py .
COPY module/module.graphql .
CMD [ "python", "./module.py" ]

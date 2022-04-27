FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip3 install --user requirements.txt
COPY ./project ./project
COPY create_tables.py .
COPY run.py .
COPY project.db .

VOLUME ["/code/project.db"]

CMD flask run -h 0.0.0.0 -p 80
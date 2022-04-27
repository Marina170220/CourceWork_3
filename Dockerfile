FROM python:3.10

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./project ./project
COPY create_tables.py .
COPY run.py .
COPY project.db .

VOLUME ["/code/project.db"]

CMD flask run -h 0.0.0.0 -p 80
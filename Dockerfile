FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get update && apt-get install -y python3-venv
RUN python3.9 -m venv /root/venv
WORKDIR /code
COPY requirements.txt /code/
RUN /root/venv/bin/pip install -r requirements.txt
COPY . /code/

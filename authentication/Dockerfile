FROM python:3.8

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt && pip install gunicorn==20.0.4

COPY . /app/

WORKDIR /app/

RUN chmod u+x ./entrypoint.sh

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
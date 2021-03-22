FROM python:3.9.2-alpine3.13
COPY *.py /
WORKDIR /triggers
COPY triggers/*.py ./
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENTRYPOINT ["/entrypoint.py"]

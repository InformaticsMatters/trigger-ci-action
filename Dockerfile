FROM python:3.9.4-alpine3.13
COPY *.py /
WORKDIR /triggers
COPY triggers/*.py ./
COPY requirements.txt /requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r /requirements.txt
ENTRYPOINT ["/entrypoint.py"]

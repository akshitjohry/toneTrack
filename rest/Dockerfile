FROM python:3.10-slim

RUN pip3 install --upgrade redis jsonpickle requests flask minio

COPY ./rest-server.py /
WORKDIR /
CMD  python3 /rest-server.py
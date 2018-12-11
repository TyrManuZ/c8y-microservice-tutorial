FROM python:3-slim

ADD webserver.py /

RUN pip install tornado

CMD [ "python", "./webserver.py" ]

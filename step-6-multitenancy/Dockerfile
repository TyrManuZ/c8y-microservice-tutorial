FROM python:3-slim

ADD webserver.py /

RUN pip install tornado
RUN pip install requests

CMD [ "python", "./webserver.py" ]

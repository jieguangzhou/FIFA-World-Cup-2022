FROM jalonzjg/dolphinscheduler-standalone-server:3.1.1-conda

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

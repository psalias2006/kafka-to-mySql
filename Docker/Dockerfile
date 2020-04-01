FROM python:3

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install -y default-libmysqlclient-dev


RUN pip install pandas
RUN pip install mysql-connector-python
RUN pip install pykafka


WORKDIR /WorkingDir

ADD kafkaBalancedConsumer .
ADD startScript .

CMD ["/bin/bash", "start.sh"]



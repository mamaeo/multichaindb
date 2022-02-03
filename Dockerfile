
# This file contains all the dependencies the Python application requires, including Python itself.

#This tells Docker to:
#   Build an image starting with the Python 3.6 image.
#   Create new directory path /usr/src/app inside docker image
#   Copy the current directory . in the project to the workdir /usr/src/app in the image.
#   Set the working directory to /usr/src/app.
#   Install required dependencies
#   Set environment variables used by the python script command.
#   Set the default command for the container to start.

FROM python:3.6
LABEL maintainer "matteo.piacentini3@studenti.unimi.it"
RUN mkdir -p /usr/src/app
COPY . /usr/src/app/
WORKDIR /usr/src/app
RUN apt-get -qq update \
    && apt-get -y upgrade \
    && apt-get install -y jq \
    && pip install . \
    && apt-get autoremove \
    && apt-get clean

VOLUME ["/data", "/certs"]

ENV PYTHONUNBUFFERED 0
ENV MULTICHAINDB_CONFIG_PATH /data/.multichaindb
ENV MULTICHAINDB_SERVER_BIND 0.0.0.0:9984
ENV MULTICHAINDB_WSSERVER_HOST 0.0.0.0
ENV MULTICHAINDB_WSSERVER_SCHEME ws
ENV MULTICHAINDB_WSSERVER_ADVERTISED_HOST 0.0.0.0
ENV MULTICHAINDB_WSSERVER_ADVERTISED_SCHEME ws
ENV MULTICHAINDB_WSSERVER_ADVERTISED_PORT 9985
ENTRYPOINT ["multichaindb"]
CMD ["start"]

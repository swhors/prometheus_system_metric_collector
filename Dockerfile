FROM ubuntu:20.04

USER root
WORKDIR /root

SHELL [ "/bin/bash", "-c" ]

RUN apt-get -qq -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install gcc g++
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install zlibc zlib1g-dev libssl-dev libbz2-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install libsqlite3-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install liblzma-dev libreadline-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install uuid-dev libffi-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq -y install make sudo bash-completion
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip

RUN apt-get -y autoclean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/python python `which python3` 1

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV WORK_HOME /opt/collector
RUN mkdir -p $WORK_HOME

ADD collector.py $WORK_HOME
ADD requirements.txt $WORK_HOME

WORKDIR $WORK_HOME
RUN pip install -r requirements.txt
EXPOSE 5001


CMD [ "python", "/opt/collector/collector.py", "-p" ]

FROM ubuntu:20.04

RUN apt-get update && \
        apt-get -y install  wget curl jq unzip git python3-pip

WORKDIR /

RUN git clone https://github.com/smk762/pytomicDEX_makerbot /opt/pytomicDEX_makerbot

WORKDIR  /opt/pytomicDEX_makerbot
RUN pip3 install -r requirements.txt

WORKDIR  /opt/pytomicDEX_makerbot/mm2
RUN wget https://github.com/KomodoPlatform/komodo-defi-framework/releases/download/v2.0.0-beta/mm2-b0fd99e84-Linux-Release.zip
RUN unzip mm2-b0fd99e84-Linux-Release.zip && unlink mm2-b0fd99e84-Linux-Release.zip

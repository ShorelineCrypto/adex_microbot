FROM ubuntu:20.04

RUN apt-get update && \
        apt-get -y install  wget curl jq unzip vim nano git python3-pip

WORKDIR /

RUN git clone https://github.com/ShorelineCrypto/adex_microbot.git /opt/adex_microbot
ENV SCRIPT_PATH=/opt/adex_microbot 


WORKDIR  /opt/adex_microbot
RUN pip3 install -r requirements.txt

WORKDIR  /opt/adex_microbot/mm2
RUN wget https://github.com/KomodoPlatform/komodo-defi-framework/releases/download/v2.0.0-beta/mm2-b0fd99e84-Linux-Release.zip
RUN unzip mm2-b0fd99e84-Linux-Release.zip && unlink mm2-b0fd99e84-Linux-Release.zip

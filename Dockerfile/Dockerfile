FROM ubuntu:20.04

RUN apt-get update && \
        apt-get -y install  wget curl jq unzip vim nano git python3-pip

WORKDIR /

RUN git clone https://github.com/ShorelineCrypto/adex_microbot.git /opt/adex_microbot


WORKDIR  /opt/adex_microbot
RUN pip3 install -r requirements.txt

## mmtools shell command is comptabile with pytomicDEX_makerbot with config of same account + netid
## however start stop must be done by microbot
WORKDIR  /root

RUN git clone https://github.com/webworker01/mmtools.git
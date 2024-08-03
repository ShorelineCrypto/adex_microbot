FROM ubuntu:20.04

RUN apt-get update && \
        apt-get -y install  wget curl jq unzip vim nano bc git python3-pip sqlite3

WORKDIR /

RUN git clone https://github.com/ShorelineCrypto/adex_microbot.git /opt/adex_microbot


WORKDIR  /opt/adex_microbot
RUN pip3 install -r requirements.txt

## python API dependencies for nonKYC exchange
RUN pip3 install aiohttp
RUN git clone https://github.com/NonKYCExchange/NonKycPythonApiClient-master
RUN cp NonKycPythonApiClient-master/nonkyc.py .

## mmtools shell command is comptabile with pytomicDEX_makerbot with config of same account + netid
## however start stop must be done by microbot
WORKDIR  /root
RUN git clone https://github.com/webworker01/mmtools.git
RUN cp /opt/adex_microbot/mmtools/* mmtools/

## mmtools can not work with DGB-segwit or USDT-PLG20 pairs
## new Komodo-defi scripts and shell to support DGB-segwit and USDT-PLG20 pairs

RUN mkdir -p  /root/atomicDEX-API/target/debug
WORKDIR /root/atomicDEX-API/target/debug
RUN wget https://raw.githubusercontent.com/KomodoPlatform/coins/master/coins
RUN git clone https://github.com/gcharang/mm2scripts
RUN cp mm2scripts/* .
RUN cp /opt/adex_microbot/mm2scripts/* .

## netid change, clean up
RUN sed -i 's/7777/8762/g' MM2_sample.json
RUN rm start.sh

## configure MM2.json, userpass files in the debug folder before running bot main.py
## rpc_password passphrase are same for legacy mmtools config file,  microbot/debug MM2.json file and debug userpass file

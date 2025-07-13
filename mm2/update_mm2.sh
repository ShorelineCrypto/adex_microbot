#!/bin/bash

rm mm2

# For release binaries
# wget $(curl -vvv https://api.github.com/repos/KomodoPlatform/komodo-defi-framework/releases | jq -r '.[0].assets | map(select(.name | contains("Linux-Release."))) | .[0].browser_download_url') -O mm2.zip
# unzip mm2.zip
# rm mm2.zip

# For mm2 binaries
wget https://github.com/KomodoPlatform/komodo-defi-framework/releases/download/v2.5.0-beta/mm2-fbab8ec85-Linux-Release.zip
unzip mm2-fbab8ec85-Linux-Release.zip 
rm mm2-fbab8ec85-Linux-Release.zip 

#!/bin/bash

rm mm2 kdf

# For release binaries
# wget $(curl -vvv https://api.github.com/repos/GLEECBTC/komodo-defi-framework/releases | jq -r '.[0].assets | map(select(.name | contains("Linux-Release."))) | .[0].browser_download_url') -O mm2.zip
# unzip mm2.zip
# rm mm2.zip

# For mm2 binaries
wget https://github.com/ShorelineCrypto/komodo-defi-framework/releases/download/v2.6.0-beta/kdf-6c02eb83e-Linux-Release_aarch64.tar.gz
tar xvfz kdf-6c02eb83e-Linux-Release_aarch64.tar.gz
rm kdf-6c02eb83e-Linux-Release_aarch64.tar.gz
ln -s kdf mm2

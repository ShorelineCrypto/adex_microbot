#!/bin/bash

rm mm2 kdf

# For release binaries
# wget $(curl -vvv https://api.github.com/repos/KomodoPlatform/komodo-defi-framework/releases | jq -r '.[0].assets | map(select(.name | contains("Linux-Release."))) | .[0].browser_download_url') -O mm2.zip
# unzip mm2.zip
# rm mm2.zip

# For mm2 binaries
wget https://github.com/GLEECBTC/komodo-defi-framework/releases/download/v2.6.0-beta/kdf_475cdb4-linux-x86-64.zip
unzip kdf_475cdb4-linux-x86-64.zip 
rm kdf_475cdb4-linux-x86-64.zip
ln -s kdf mm2

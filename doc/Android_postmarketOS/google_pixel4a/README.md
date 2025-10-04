
# PostmarketOS - Google Pixel 4a

PostmarketOS only support Google Pixel 4a on CLI command line interface with no working touch screen, no GUI, nor wifi support. However, this bare bone support is good enough as USB connection between a linux server host and phone would be enough to allow bare bone postmarketOS on google pixel 4a to connect to internet through NAT. 

Follow this detailed page guide to install CLI only bare bone postmarketOS into old google pixel 4a:
https://wiki.postmarketos.org/wiki/Google_Pixel_4a_(google-sunfish)


## Trouble Shooting after PostmarketOS Installation

Assuming you have successfully flashed and install postMarketOS on google pixel 4a, the touch screen is not working, and GUI/wifi nothing works. However, you can 
typically rely on USB connection between linux host and android phone to finish the work. 

### Login into Pixel 4a Linux through USB

Typically, USB is automatically connected between linux server and your google pixel 4a alpine linux. Run below to login into phone:
```commandline
ssh user@172.16.42.1
```

'user' is the username you setup during postmarketOS installation step above.  Typically, after phone reboot, you can login into phone using this command and IP address. However, the phone has no internet access other than internal connection to your linux server through USB. 

### Set up NAT internet connection through USB

Follow this postmarketOS USB networking guide: 
https://wiki.postmarketos.org/wiki/USB_Internet

This page explains how you can configure USB internet NAT so that your google pixel 4a device on bare bone postmarketOS can connect to internet and use docker pull down images. 

The helper scripts for Google Pixel 4a model is provided for setting up internet on USB.

### Install adex_microbot in postmarketOS phone

Docker should be installed by default inside postmarketOS.  Now you should be able to pull down docker image on arm64 hardware and follow this repo to run containers on regular/AMM pool bot, or arbitrage bot.

### Resolve battery charging issue

By default, the postmarketOS installed on google pixel 4a will die and reboot in 2 or 3 days due to out of battery. The battery auto charging is not supported by default. 

However, you can enable google pixel 4a on postmarketOS to be properly charged with no reboot by installing Android SDK platform-tools daemon by running below:
```commandline
  adb devices
  fastboot devices
```

The above two commands will start adb daemon in the host linux server with USB connected to the phone. The above command may not show any android device listed, which is fine. With adb daemon running on linux host with USB connection to the phone, the postmarketOS phone battery will be recharged automatically on USB.

# PostmarketOS - Google Pixel 4a

PostmarketOS only support Google Pixel 4a on CLI command line interface with no working touch screen, no GUI, nor wifi support. However, this bare bone support is good enough as USB connection between a linux server host and phone would be enough to allow bare bone postmarketOS on google pixel 4a to connect to internet through NAT. 

Follow this detailed page guide to install CLI only bare bone postmarketOS into old google pixel 4a:
https://wiki.postmarketos.org/wiki/Google_Pixel_4a_(google-sunfish)

## Flashing qcom-sm7150 Steps

The Google Pixel 4a first need to be flashed into QCOM SM7150 postmarketOS. However 'cache' partition does not exist. So there will be errors on the above guide. 
Below are high level working steps to complete PostmarketOS installation into Google Pixel 4a
1. unlock the phone bootloader, follow google/youtube guides, with developer mode USB connected to linux Ubuntu 22.04 or 24.04 desktop as host server.
2. On linux host USB connected to your pixel 4a phone, install adb/fastboot properly, configure your non-root account to be able to run "fastboot devices" to see your phone.
3. Clear our phone partitions with below commands on linux host terminal:
```commandline
fastboot devices
fastboot erase dtbo
fastboot erase boot
fastboot erase  boot_b
fastboot erase  userdata
```
Ensure above commands run with no errors operating on your USB connected google pixel 4a. Note that pixel 4a has no 'cache' partition, instead it use boot (boot_a) partition for U-boot and boot_b serving as cache. 
4. Installing U-Boot step.
5. Installing pmbootstrap step.
pmbootstrap require non-root user to run. pmboobstrap init Q/A steps use below configurations: channel - stable version, console, using your ssh pub key for login, etc. It will generate two images, boot and root, then flash. The pmbootstrap flashing step will fail on 'cache' partition.
go to pmboobstrap folder that generated image files: `qcom-sm7150-boot.img` `qcom-sm7150-root.img`, then:
5. Flash on pmboobstrap image files with below command:

```commandline
fastboot flash boot_b qcom-sm7150-boot.img
fastboot flash userdata qcom-sm7150-root.img
fastboot devices
fastboot reboot
```
Now your google pixel4a should reboot to postmarketOS console for login. We use ssh to login into phone remotely from host linux server.
## Trouble Shooting after PostmarketOS Installation

Assuming you have successfully flashed and installed postMarketOS on google pixel 4a, the touch screen is not working, and GUI/wifi nothing works. However, you can 
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
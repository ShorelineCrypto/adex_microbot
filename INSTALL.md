# Installation Guide for adex_microbot

For high level understanding of PytomicDEX Makerbot that this code base forked from, please checkout file "orig-README.md" which explains well on understanding of the bot software.

adex_microbot added new features as listed in README page and will be explained in details below

Specifically, for adex_microbot software set up, please follow below steps to start Nengcoin and Cheetahcoin market making bot quickly in Komodo Wallet / AtomicDEX.

## Hardware Requirement - X86_64, Arm64 Linux, Android Phone, Raspberry pi

The whole package was tested successfully in linux on x64 and arm64 hardware with docker.  Rooted android phone that can install ubuntu 20.04 inside phone can work well too
as the single docker image is built on Ubuntu 20.04, so does rasberry pi on Ubuntu 20.04. For rooted android phone or rasberry pi instalaltion of adex_microbot, checkout the
file "adex_microbot/Dockerfile/Dockerfile" for instalaltion steps on rooted android phone or Pi on Ubuntu 20.04.


## Requirement - Linux, Docker
The source code adex_microbot has been successfully tested in Ubuntu 18.04 / 20.04, MX Linux / Debian bookworm with docker installed.

In general in ubuntu or debian linux, please follow below to install docker:
```
  sudo apt-get update
  sudo apt-get install docker.io
```


## Step 1 - build/run adex_microbot docker image

To build your own adex_microbot image, run below:

```
  git clone https://github.com/ShorelineCrypto/adex_microbot.git
  cd adex_microbot/Dockerfile
  docker build -t  adex_microbot .
```

Alternatively, you can download a working docker image from docker hub:

```
  docker pull shorelinecrypto/adex_microbot:latest
  docker tag shorelinecrypto/adex_microbot:latest adex_microbot
```

#
## Step 2 - Start adex_microbot container

adex_microbot container runs in command terminal. Therefore, it is better to use screen or tmux session to run below in the background. 

now start bot container as below command:
```
  docker run -it --name adexbot adex_microbot:latest /bin/bash
```
If above command runs successfully, a container prompt will show up inside your screen or tmux session like below:

```
root@ae6706bd8c07:~/atomicDEX-API/target/debug#
```

You now can run or manage below steps within container.  Screen or tmux session should allow you easily get back to linux host terminal if needed.

## Step 3 - Configure atomicDEX Komodo-defi (MM2) account

mmtools or pymakerbot uses same style of komod-defi-framework or mm2 account with username and password.  Use below command you can easily generated a mm2 account:
```
root@ae6706bd8c07:~/atomicDEX-API/target/debug# cd ~/mmtools
root@ae6706bd8c07:~/mmtools# ./init 
No config file detected, do you want to set one up? (y/n)y
Generate random wallet passphrase? (y/n)y
Generate random rpc userpass? (y/n)y
Install atomicDEX-API and dependencies? (y/n)n
Install cipi's mmtools/mpm and dependencies? (y/n)n
root@ae6706bd8c07:~/mmtools#
```

The above mmtools operation will generate a komodo-defi or mm2 account inside "config' file in above folder. mmtools is still under legacy Komodo-defi style so that its generated account
need a special character (like % * etc characters) to be inserted into password. Use your favorite editor nano or vi to modify the file "config", insert an character "%" inside
field word afer "userpass=xxxxx".  Please note that pair of fields "passphrase" "userpass" are your komodo-defi trading bot private key. If you lose them, you lose all the coins under this
mm2 account.

Now enable KMD NENG and CHTA coins in mmtools. Modify "config" file below and change the coin to NENG and CHTA:


```
# Auto connect to these electrums on ./start (requires automation=1)
auto_enable=('KMD' 'VRSC' 'WSB' 'SOULJA')
```

After change, the "config" file should like this:

```
# Auto connect to these electrums on ./start (requires automation=1)
auto_enable=('KMD' 'NENG' 'CHTA')
```

Now go to below, copy the "userpass" field value into debug folder file below:
```
cd ~/atomicDEX-API/target/debug
root@ae6706bd8c07:~/atomicDEX-API/target/debug# more userpass 
userpass=RPC_CONTROL_USERPASSWORD
root@ae6706bd8c07:~/atomicDEX-API/target/debug#
```

Modify above "userpass" file, copy the "config" file userpass value and replace that the word "RPC_CONTROL_USERPASSWORD" above word with actual config file value for this field.
Now the mmtools configuration is complete.


## Step 4 - Configure PytomicDEX Makerbot Settings

Inside container, now use the mmtools same account for makerbot:

```
 cd /opt/adex_microbot/config
 root@ae6706bd8c07:/opt/adex_microbot/config# cp MM2.json-example  MM2.json        
root@ae6706bd8c07:/opt/adex_microbot/config# 
```

use vi or nano to modify the above "MM2.json" file,  copy the userpass value from mmtools config file into the field "rpc_password". Copy the same "passphrase"
field value to replace json file value too. Save

## Step 5 - Start/stop Makerbot, Activate DGB

Now configura and start and stop Makerbot

```
  root@ae6706bd8c07:/opt/adex_microbot# ./makerbot.py
  coins file not found, downloading...
Enter tickers of coins you want to sell, seperated by a space (default: KMD CHTA):
KMD CHTA NENG
Enter tickers of coins you want to buy, seperated by a space (press enter to use same coins as above):

Enter default minimum trade value in USD (default: $0.1): 

```

The rest questions can be default, makerbot won't run, this above is just a configuration and start bot.  When first time you run the makerbot, the
mm2 binary file is not found, and the bot will automatically download x64 binary copy for that.

Then start Makerbot by selecting [0] Start Makerbot, this will activate KMD NENG CHTA and bot too.  After that, select [3] Stop Makerbot to stop running Makerbot.
For adex_microbot, we only use wallet service of makerbot, not actually want to run this makerbot (won't work on NENG or CHTA anyway).

You then try to select (4) Activate Coins
type "DGB-segwit" to activate DGB.  In newer version of Komodo wallet, DGB is wallet only, only the segwit address of DGB can allow DEX trading.

The finally, select [9] Loop Views  to view your Makerbot settings, and find your KMD NENG CHTA DGB-segwit address.  You can deposit coins into these addresses.

Finally, Ctrl-C and select [11] to exit Makerbot:
```
[10] Withdraw Funds
 [11] Exit TUI
 Select menu option: 11

Stop Komodo DeFi Framework on exit? [Y/N]: N 
root@ae6706bd8c07:/opt/adex_microbot# 
```

## Optional Step 6 - mm2 binary Download for arm64

For x64, mm2 working binary file will be downloaded from Komodo github automatically by Makerbot above. For arm64 hardware, Komodo github does not have compiled working mm2 binary file so that
above step 5 would crash. Run below in container for arm64 platform to download a working mm2 binary file compiled by ShorelineCrypto:
```
cd /opt/adex_microbot/mm2
root@arm64container:/opt/adex_microbot/mm2# wget https://github.com/ShorelineCrypto/komodo-defi-framework/releases/download/v2.0.0-beta/mm2-b0fd99e84-Linux-Release_aarch64.tar.gz
root@arm64container:/opt/adex_microbot/mm2# tar xvfz mm2-b0fd99e84-Linux-Release_aarch64.tar.gz && rm mm2-b0fd99e84-Linux-Release_aarch64.tar.gz
```

The above command should download arm64 version of mm2 binary from ShorelineCrypto and unpack the file "mm2" into proper folder.  You can now go back to Step 5 and complete that step.


## Step 7 - Deposit Coins, Start Bot

From loop view, you can get all your addresses for KMD, NENG, CHTA and DGB-segwit,  deposit proper worth of coins into each, wait for confirmation to be confirmed in your address.

You can now start adex_microbot market making bot pairs on NENG/KMD CHTA/KMD  NENG/DGB  and CHTA/DGB pairs. By the default, adexbot will place $0.05 USD worth of amount of value of
coins into each pair and refresh pairs in 3 minutes on latest market pricing.

```
  cd /opt/adex_microbot/
  ./start_microbot.sh &
```

## Step 8 - Monitor and Backup

Maker sure you back up your mm2 account information somewhere.

For monitor your trading bot actions, you can check log file at:
```
  cd ~
  more main.log
  cd mmtools
  ./my_recent_swaps
  ./orderbook KMD CHTA
   ./orderbook DGB NENG
   cd ~/atomicDEX-API/target/debug/
   ./mybalance.sh DGB-segwit | jq .
```

Please check mmtools github repo and atomicDEX-api tutorial page from Komodo platform for more details of command line operations. You should now have full function
of adex_microbot providing liquidity for Nengcoin and Cheetahcoin at Komodo Wallet / AtomicDEX.








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

Alternatively, you can download a working docker image from docker hub,

x64 linux:
```
  docker pull shorelinecrypto/adex_microbot:amd64
  docker tag shorelinecrypto/adex_microbot:amd64 adex_microbot
```

arm64 linux:
```
  docker pull shorelinecrypto/adex_microbot:arm64
  docker tag shorelinecrypto/adex_microbot:arm64 adex_microbot
```

## Step 2 - Start adex_microbot container

adex_microbot container runs in command terminal. Therefore, it is better to use screen or tmux session to run below in the background. The code base currently has two running
mode: liquidity pool mode or arbitrage bot mode. It is recommended to run two separate docker containers if both pool/arb bots are run. 

now start pool bot container as below command:
```
  docker run -it --name poolbot adex_microbot:latest /bin/bash
```
If above command runs successfully, a container prompt will show up inside your screen or tmux session like below:

```
root@ae6706bd8c07:~/atomicDEX-API/target/debug#
```

To start arbitrage bot in same server, just start with another container name in different screen/tmux session terminal:

```
  docker run -it --name arbbot adex_microbot:latest /bin/bash
```

In either cases, poolbot or arbitrage bot, then run below commands to get latest commits of code in container:

```
  cd  /opt/adex_microbot
  git pull
```

Nengcoin and cheetahcoin are traded at Centralized Exchange (CEX) nonKYC exchange. When CEX API config profile is configured properly, a hedging trade on either NENG/DOGE or CHTA/DOGE pair in CEX will be placed
automatically after completion of each atomicDEX trade in the arbitrage bot mode. 

When you run two bots on arb + pool mode, the two containers should create their own different mm2 account as shown below with same steps. 

You now can run or manage below steps within container.  Screen or tmux session should allow you easily get back to linux host terminal if needed.

## Step 3 - Configure atomicDEX Komodo-defi (MM2) account / NetID

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

The legacy mmtools config file has old netID 7777, make sure you modify Net ID into current like below:
```
netid=8762
```

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
 cd /opt/adex_microbot
 cp activate_commands.json-example activate_commands.json
 cd /opt/adex_microbot/config
 root@ae6706bd8c07:/opt/adex_microbot/config# cp MM2.json-example  MM2.json        
root@ae6706bd8c07:/opt/adex_microbot/config# 
```

use vi or nano to modify the above "MM2.json" file,  copy the userpass value from mmtools config file into the field "rpc_password". Copy the same "passphrase"
field value to replace json file value too. Save

Make sure copy a working "MM2.json" file to ~/atomicDEX-API/target/debug folder for mm2scripts operations. 

## Step 5 - mm2 binary Download for arm64 or x64

For x64 hardware, run below in container to download and install a working mm2 binary file compiled by Komodo Platform dev team:
```
cd /opt/adex_microbot/mm2
root@arm64container:/opt/adex_microbot/mm2# bash update_mm2.sh
```

For arm64 hardware, Komodo github does not have compiled working mm2 binary file, but instead we run below in container for arm64 platform
to download a working mm2 binary file compiled by ShorelineCrypto dev team:
```
cd /opt/adex_microbot/mm2
root@arm64container:/opt/adex_microbot/mm2# bash update_mm2_arm64.sh
```

The above command should download x64 or arm64 version of mm2 binary from komodo or ShorelineCrypto and unpack the file "mm2" into proper folder.
You can run below to confirm the version of mm2 binary:

```
  ./mm2 --version
```


## Step 6 - Start/stop Makerbot, Activate DGB

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
type "USDT-PLG20" and "MATIC" to activate USDT on polygon (MATIC) network. USDT-PLG20 gas fees are paid on MATIC so that both are enabled. 

The finally, select [9] Loop Views  to view your Makerbot settings, and find your KMD NENG CHTA DGB-segwit MATIC USDT-PLG20 address.  You can deposit coins into these addresses.

Finally, Ctrl-C and select [11] to exit Makerbot:
```
[10] Withdraw Funds
 [11] Exit TUI
 Select menu option: 11

Stop Komodo DeFi Framework on exit? [Y/N]: N 
root@ae6706bd8c07:/opt/adex_microbot# 
```

## Step 7 - Arbitrate Bot CEX API configuration

This step is only required if you are running arbitrage bot. This step is not needed for pool bot. 

Arbitrage bot mode needs configuration of CEX API configuration. For Cheetahcoin or Nengcoin, nonKYC exchange is the main centralized exchange (CEX) so that API keys/secrets need to
be enabled at nonKYC web account first.  Enable all the API functions except that withdraw access. Copy down access key and secret key. 

Run below inside arbbot container:

```
  docker exec -it arbbot /bin/bash
  root@c79ae11f1c8f:~/atomicDEX-API/target/debug# cd /opt/adex_microbot/config
  root@c79ae11f1c8f:/opt/adex_microbot/config# cp nonkyc_settings.json-example  nonkyc_settings.json
```

Use linux vi or nano editor to modify the "nonkyc_settings.json" file, fill in the correct information for our CEX account on  "access_key" and "secret_key"
fields values, then save the file.

Then setup the arb.db sqlite3 database:

```
  cd /opt/adex_microbot/arbitragedb
root@c79ae11f1c8f:/opt/adex_microbot/arbitragedb  sqlite3 arb.db < arbitragedb_schema.sql
```

This above command will create a table "swaps_arbitrage" within sqlite3 arb.db database.  The arbitrage python code will check the completed atomicdex swap on
MM2 sqlite3 database and then write CEX hedging calculation results into this arb.db table for log tracking, and then execute API hedging trade in nonKYC exchange.

## Step 8 - Deposit Coins, Start Bot

From loop view, you can get all your addresses for KMD, NENG, CHTA and DGB-segwit,  deposit proper worth of coins into each, wait for confirmation to be confirmed in your address.

For trading on USDT-PLG20 pairs, you can obtain initial amount of Polygon MATIC from community run atomicDEX gas station: https://dexstats.info/gas.php, 
then deposit proper USDT on polygon (MATIC) network into your USDT-PLG20 address.  The MATIC address and USDT-PLG20 should have same address in your wallet. 

You can now start adex_microbot market making liquidity pool bot on NENG/KMD, CHTA/KMD, NENG/DGB-segwit, and CHTA/DGB-segwit pairs. By the default, adexbot pool will place curve shaped USD worth of
coins into each pair and refresh pairs in 3 minutes on latest market pricing.

#### liquidity pool bot

```
  cd /opt/adex_microbot/
  ./start_abot_pool.sh &
```

The above will run liquidity pool without USDT pair.  To include USDT-PLG20 pair in your liquidity pool, run below command instead:
```
  cd /opt/adex_microbot/
  ./start_abot_pool_withUSDT.sh &
```

Either of the above pool shell scripts runs abot_pool.py for placing pool trading pairs. Run command "abot_pool.py --help" to see how you can control pool base_spread / USD_unit
by modifying the shell script above. 

#### arbitrage bot

Aternatively, instead of running liquidity pool bot above, you can run arbitrage bot mode where by default 1 pair each of KMD/CHTA, KMD/NENG, DGB-segwit/CHTA,
DGB-segwit/NENG, USDT-PLG20/CHTA, USDT-PLG20/NENG  with $1.0 USD worth of coins on +-2% of bid/ask spread will be placed.

Run arb bot, refresh every 3 minutes:
```
  cd /opt/adex_microbot/
  ./start_arbitrage_bot.sh &
```
   type "./arbitrage.py --help" to see how you can control base_spread / USD_unit on this command. 

If you configure the nonKYC exchange CEX config file correctly, a corresponding hedging trade willl be placed upon completion of each atomicDEX swap.

To properly operate arbitrage bot hedging function, make sure you deposit enough coins at nonKYC exchange on DOGE, NENG and CHTA balances to allow hedging execution to
succeed. 


## Step 9 - Monitor and Backup

Maker sure you back up your mm2 account information somewhere.

For monitor your trading bot actions, you can check log files, or running mmtools or mm2scripts commands:
```
  cd ~
  more pool.log
  more arb.log
  cd mmtools
  ./my_recent_swaps
  ./orderbook KMD CHTA
   ./orderbook DGB NENG
   cd ~/atomicDEX-API/target/debug/
   ./mybalance.sh DGB-segwit | jq .
   cd /opt/adex_microbot
   ./loop_views.py
```

Please check mmtools github repo and atomicDEX-api tutorial page from Komodo platform for more details of command line operations. You should now have full function
of adex_microbot providing liquidity for Nengcoin and Cheetahcoin at Komodo Wallet / AtomicDEX.








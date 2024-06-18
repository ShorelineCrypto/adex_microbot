
# adex_microbot - AtomicDEX Trading Bot for Cheetahcoin and Nengcoin
#### Not Your Keys, Not your Coins
#### Decentralization, Own your Private Keys with Komodo Wallet / AtomicDEX
#### Suitable for micro trading market making on CHTA and NENG on KMD, DGB-segwit or USDT pairs
#### Automatic start/stop scripts for liquidity pool or arbitrage mode

Komodo wallet (Mobile on Android/iOS, Desktop on Windows/MacOS/Linux) has its built-in atomic swap based decentralized exchange (DEX) atomicDEX that is very
suitable for trading on small dollar amount with low fees. Because Nengcoin or Cheetahcoin has fast and consistant block time, a typical trade on supported pair can be
done between 10 minutes to 1 hour time frame. 

Adex_microbot is fork of PytomicDEX Makerbot for the purpose of micro trading bot on Cheetahcoin and Nengcoin in Komodo Wallet / AtomicDEX.
Currently it supports CHTA/KMD, CHTA/DGB-segwit, CHTA/USDT-PLG20, NENG/KMD, NENG/DGB-segwit, NENG/USDT-PLG20 6 trading pairs in default settings.

Although atdex_microbot is coded only for Cheetahcoin and Nengcoin, this pierce of open sourced code can be forked off and adapted for any other
coins in Komodo Wallet for automatic market making bot.

### Features of adex_microbot

1. Linux on both X64 or Arm64 hardware platform are supported so that adex_microbot can be run remotely automatically in cheap rented cloud platform. 
2. Liquidity pool: 1 pair of DGB and USDT orders with +-%1 spread and 3 pairs of KMD orders with +-1% +-2% +-3% spreads are coded at fixed USD worth of coins amount. Trading amount on USD amount and spread are configurable.
3. Arbitrage bot:  default +- 10% spread, $1.0 USD worth of coins amount. Trading amount on USD amount and spread are configurable.
4. The market pricing of NENG and CHTA come from nonKYC Exchange DOGE pairs because PytomicDEX at currrent version does not provide smaller coins (NENG or CHTA)
accurate wallet/DEX market price. CEX doge pairs real time market pricing is selected because both coins have higher CEX liquidity on DOGE pair than USDT pair.
5. abot_pool.py / arbitrage.py as main bot control code to replace PytomicDEX bot start/stop/setup functions. For this code, only wallet feature of PytomicDEX is used while the original PytomicDEX DEX trading feature is
not used or disabled.  This is because PytomicDEX original code does not have working bot trading functions for Cheetahcoin or Nengcoin.
6. mmtools and mm2scripts code base are incorporated into this code base.  The mmtools inside adex_microbot can provide more user friendly manual command line control of atomicDEX trading on KMD pairs while mm2scripts is
used for fast order execution and/or segwit coin order book operations.

License
-------
Released under the GNU General Public License v2

http://www.gnu.org/licenses/gpl-2.0.html

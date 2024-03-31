
# adex_microbot - AtomicDEX Trading Bot for Cheetahcoin and Nengcoin
#### Not Your Keys, Not your Coins
#### Decentralization, Own your Private Keys with Komodo Wallet / AtomicDEX
#### Suitable for micro trading market making on CHTA/KMD CHTA/DGB NENG/KMD NENG/DGB

Adex_microbot is fork of PytomicDEX Makerbot for the purpose of micro trading bot on Cheetahcoin and Nengcoin in Komodo Wallet / AtomicDEX.
Currently it supports CHTA/KMD, CHTA/DGB-segwit, NENG/KMD, NENG/DGB-segwit 4 trading pairs in default settings.

Although atdex_microbot is coded only for Cheetahcoin and Nengcoin, this pierce of open sourced code can be forked off and adapted for any other
coins in Komodo Wallet for automatic market making bot.

### Features of adex_microbot

1. 1 pair of DGB orders with +-%1 spread and 3 pairs of KMD orders with +-1% +-2% +-3% spreads are coded at fixed $0.05 USD worth of coins amount.
2. The market pricing of NENG and CHTA come from nonKYC Exchange DOGE pairs because PytomicDEX at currrent version does not provide smaller coins (NENG or CHTA)
accurate wallet/DEX market price. CEX doge pairs real time market pricing is selected because both coins have higher CEX liquidity on DOGE pair than USDT pair.
3. main.py as main bot control code to replace PytomicDEX bot start/stop/setup functions. For this code, only wallet feature of PytomicDEX is used while the original PytomicDEX DEX trading feature is
not used for disabled.  This is because PytomicDEX original code does not have working bot trading functions for Cheetahcoin or Nengcoin.
4. mmtools code base is incorporated into this code base as mmtools inside adex_microbot can provide more user friendly manual command control of atomicDEX trading on KMD pairs.

License
-------
Released under the GNU General Public License v2

http://www.gnu.org/licenses/gpl-2.0.html

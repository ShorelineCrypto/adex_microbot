
# adex_microbot - AtomicDEX Trading Bot for Cheetahcoin and Nengcoin
#### Not Your Keys, Not your Coins
#### Decentralization, Own your Private Keys
#### Suitable for micro trading market making in Komodo Wallet / AtomicDEX

Adex_microbot is fork of PytomicDEX Makerbot for the purpose of micro trading bot on Cheetahcoin and Nengcoin in Komodo Wallet / AtomicDEX.
Currently it supports CHTA/KMD, CHTA/DGB-segwit, NENG/KMD, NENG/DGB-segwit 4 trading pairs in default settings.

Although atdex_microbot is coded only for Cheetahcoin and Nengcoin, this pierce of open sourced code can be forked off and adapted for any other
coins in Komodo Wallet for automatic market making bot.

### Features of adex_microbot

1. 3 pairs of KMD orders with each order at fixed $0.05 USD value.
2. The market pricing of NENG and CHTA come from nonKYC exchange DOGE pairs because PytomicDEX at currrent version does not provide smaller coins (NENG or CHTA)
accurate wallet/DEX market price. NonKYC doge pairs real time exchange pricing is selected as both have higher CEX liquidity on DOGE pairs.
3. main.py as main bot control code. PytomicDEX has its own bot start/stop setup. For this code, only wallet feature of PytomicDEX is used while the DEX trading feature is disabled as
the default PytomicDEX trading bot configuration is mainly for OG biggers coins, not for smaller coin microbot trading. 
4. mmtools codes are incorporated into this code base as mmtools inside adex_microbot can provide more user friendly manual control on the trading pairs.

License
-------
Released under the GNU General Public License v2

http://www.gnu.org/licenses/gpl-2.0.html

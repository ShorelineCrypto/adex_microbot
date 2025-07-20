select * from swaps_arbitrage where is_success = 1 ;
select * from swaps_arbitrage where is_success = 0 ;
select coin, sum(quantity) from  net_unhedged where coin = 'CHTA' ;
select coin, sum(quantity) from  net_unhedged where coin = 'NENG' ;
select * from remainder_swaps_arbitrage ;
select * from cex_session ;

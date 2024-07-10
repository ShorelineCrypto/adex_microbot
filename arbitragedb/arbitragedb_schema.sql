CREATE TABLE swaps_arbitrage (
    id INTEGER NOT NULL PRIMARY KEY,
    market VARCHAR(255) NOT NULL,
    side VARCHAR(255) NOT NULL,
    quantity DECIMAL NOT NULL,
    price DECIMAL NOT NULL,
    uuid VARCHAR(255) NOT NULL UNIQUE,
    started_at INTEGER NOT NULL,
    finished_at INTEGER NOT NULL,
    arb_market VARCHAR(255) NOT NULL,
    arb_price DECIMAL NOT NULL,
    is_success INTEGER NOT NULL DEFAULT 0,
    maker_pubkey VARCHAR(255),
    taker_pubkey VARCHAR(255));
CREATE INDEX timestamp_index ON swaps_arbitrage (started_at);


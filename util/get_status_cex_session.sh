#! /bin/bash

sqlite3 /opt/adex_microbot/arbitragedb/arb.db  < /opt/adex_microbot/arbitragedb/status_cex_session.sql

#! /bin/bash

MM2_DB_FILE=`/path/to/DB/folder/*/MM2.db`
sqlite3 $MM2_DB_FILE < /opt/adex_microbot/ammpool/get_uuid_failed_swap.sql > failed_uuid

for uuid in `cat failed_uuid`
do
  echo $uuid
  /opt/adex_microbot/ammpool/manual_recover_fund.sh $uuid
done

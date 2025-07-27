for uuid in `cat failed_uuid-07262025`
do
  echo $uuid
  ./manual_recover_fund.sh $uuid
done

#!/bin/bash
bash tmp_gnd/gnd_reset.sh

./manage.py sync_investors
./manage.py sync_involvements
./manage.py sync_deals

#psql -U landmatrix landmatrix -c "update landmatrix_historicalactivityattribute set date='2007-09-30' where name='implementation_status' and date='2007-09-31'"
#
## elastic stuff
#python << EOF
##x = {
##"contract_area": [1141,1149,3796,4372,4990,5015,6696,6829,7057,7074,7152,7246,7395,7716,],
##"production_area": [1141,3506,3509,3548,3558,3568,3569,3642,4953,6939,6828,7602,7604,7609,],
##"intended_area": [7393,7395]
##}
#x = {
#"contract_area": [1141,1149,3796,6829,7057,7074,7246,7395,7716,],
#"production_area": [1141,4953,6939,6828,],
#"intended_area": [7393]
#}
#
#[Location.objects.filter(deal_id__in=v).update(**{k:None}) for k,v in x.items()]
#
#
#EOF
#
#./manage.py search_index --rebuild -f
#
## then turn on the celery task runner

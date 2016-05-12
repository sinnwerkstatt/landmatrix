#!/usr/bin/env bash

function collect_failed() {
    for id in $(psql -Ulandmatrix landmatrix_2 -t -c "select distinct activity_identifier from landmatrix_activity where fk_status_id in (2,3) order by activity_identifier;"); do
        echo $id $(wget --spider http://localhost:8000/deal/$id/ 2>&1 | grep 'HTTP') | grep -v '200 OK'
    done > errors.txt
}

for line in $(cat errors.txt | cut -d ' ' -f 1); do
    wget -o - -O - http://landmatrix.org/en/get-the-detail/all/all-deals/$line/ | grep 'Deal not found' >/dev/null || echo $line
done

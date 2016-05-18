#!/usr/bin/env bash

LOGFILE_NAME=errors.txt
function collect_failed() {
    for id in $(psql -Ulandmatrix landmatrix_2 -t -c "select distinct activity_identifier from landmatrix_activity where fk_status_id in (2,3) order by activity_identifier;"); do
        echo ${id} $(wget --spider http://localhost:8000/deal/${id}/ 2>&1 | grep 'HTTP') | grep -v '200 OK'
    done > ${LOGFILE_NAME}
}

for id in $(cat ${LOGFILE_NAME} | cut -d ' ' -f 1); do
    wget -o /dev/null -O - http://landmatrix.org/en/get-the-detail/all/all-deals/${id}/ | \
        grep 'Deal not found' >/dev/null || echo ${id}
done

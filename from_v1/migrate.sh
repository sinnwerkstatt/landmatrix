#!/usr/bin/env bash

pg_dump -Uroot --column-inserts -a -t regions landmatrix_1 | \
    sed s/regions/landmatrix_region/g > regions.sql

pg_dump -Uroot --column-inserts -a -t countries landmatrix_1 | \
    sed s/countries/landmatrix_country/g | \
    sed s/fk_region/fk_region_id/g > countries.sql

pg_dump -Uroot --column-inserts -a -t activities landmatrix_1 | \
    sed s/activities/landmatrix_activity/g | \
    sed s/fk_status/fk_status_id/g > activities.sql

pg_dump -Uroot --column-inserts -a -t stakeholders landmatrix_1 | \
    sed s/stakeholders/landmatrix_stakeholder/g | \
    sed s/fk_status/fk_status_id/g > stakeholders.sql

pg_dump -Uroot --column-inserts -a -t primary_investors landmatrix_1 | \
    sed s/primary_investors/landmatrix_primaryinvestor/g | \
    sed s/fk_status/fk_status_id/g > primary_investors.sql

pg_dump -Uroot --column-inserts -a -t involvements landmatrix_1 | \
    sed s/involvements/landmatrix_involvement/g | \
    sed s/fk_activity/fk_activity_id/g  | \
    sed s/fk_stakeholder/fk_stakeholder_id/g  | \
    sed s/fk_primary_investor/fk_primary_investor_id/g > involvements.sql

pg_dump -Uroot --column-inserts -a -t languages landmatrix_1 | \
    sed s/languages/landmatrix_language/g | \
    sed s/fk_stakeholder/fk_stakeholder_id/g | \
    sed s/fk_language/fk_language_id/g  > languages.sql

pg_dump -Uroot --column-inserts -a -t stakeholder_attribute_groups landmatrix_1 | \
    sed s/stakeholder_attribute_groups/landmatrix_stakeholderattribute/g | \
    sed s/fk_stakeholder/fk_stakeholder_id/g | \
    sed s/fk_language/fk_language_id/g > stakeholder_attribute_groups.sql

pg_dump -Uroot --column-inserts -a -t activity_attribute_groups landmatrix_1 | \
    sed s/activity_attribute_groups/landmatrix_activityattribute/g | \
    sed s/fk_activity/fk_activity_id/g | \
    sed s/fk_language/fk_language_id/g | \
    sed 's/ year, / date, /g' > activity_attribute_groups.sql

cp activity_attribute_groups.sql activity_attribute_groups.sql.1901

for i in `eval echo {1901..2016}`; do
    echo $i
    cat activity_attribute_groups.sql.$i | \
        sed "s/, $i, /, \'$i-01-07\', /g" > activity_attribute_groups.sql.$[$i+1]
done && \
    mv activity_attribute_groups.sql.2017 activity_attribute_groups.sql && \
    rm -f activity_attribute_groups.sql.????


# status table has already been filled by a fixture

for sqlfile in regions countries activities stakeholders primary_investors \
               languages stakeholder_attribute_groups activity_attribute_groups ; do
    psql -Ulandmatrix landmatrix_2 < ${sqlfile}.sql
done




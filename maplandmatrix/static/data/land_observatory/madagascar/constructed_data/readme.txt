Use pg_restore to populate database.

Add constructed Activities:
curl -u "admin:password" -d @lmkp/documents/madagascar/constructed_data/constructed_activities.json -H "Content-Type: application/json" http://localhost:6543/activities

Add constructed Stakeholders:
curl -u "admin:password" -d @lmkp/documents/cambodia/constructed_data/constructed_stakeholders.json -H "Content-Type: application/json" http://localhost:6543/stakeholders

Set them active:
-- Activities
-- Set them all to 'inactive'
UPDATE data.activities
SET fk_status = 3
WHERE activity_identifier IN
	(
                '1abcdef1-abcd-abcd-abcd-abcdefabcde1',
		'1abcdef1-abcd-abcd-abcd-abcdefabcde2',
		'1abcdef1-abcd-abcd-abcd-abcdefabcde3'
	);
-- Set the latest version of each Activity to 'active'
UPDATE data.activities
SET fk_status = 2
WHERE id IN (
        SELECT b.id
        FROM (
                SELECT activity_identifier, max(version) AS maxversion
                FROM data.activities
				WHERE activity_identifier IN
					(
                                            '1abcdef1-abcd-abcd-abcd-abcdefabcde1',
                                            '1abcdef1-abcd-abcd-abcd-abcdefabcde2',
                                            '1abcdef1-abcd-abcd-abcd-abcdefabcde3'
					)
                GROUP BY activity_identifier
        ) AS a
        INNER JOIN data.activities AS b ON b.activity_identifier = a.activity_identifier AND b.version = a.maxversion
);
-- Stakeholders
-- Set them all to 'inactive'
UPDATE data.stakeholders
SET fk_status = 3
WHERE stakeholder_identifier IN
	(
                'a1234567-1234-1234-1234-12345678912a',
		'a1234567-1234-1234-1234-12345678912b',
		'a1234567-1234-1234-1234-12345678912c',
		'a1234567-1234-1234-1234-12345678912d',
		'a1234567-1234-1234-1234-12345678912e',
		'a1234567-1234-1234-1234-12345678912f'
	);
-- Set the latest version of each Stakeholder to 'active'
UPDATE data.stakeholders
SET fk_status = 2
WHERE id IN (
        SELECT b.id
        FROM (
                SELECT stakeholder_identifier, max(version) AS maxversion
                FROM data.stakeholders
				WHERE stakeholder_identifier IN
					(
                                            'a1234567-1234-1234-1234-12345678912a',
                                            'a1234567-1234-1234-1234-12345678912b',
                                            'a1234567-1234-1234-1234-12345678912c',
                                            'a1234567-1234-1234-1234-12345678912d',
                                            'a1234567-1234-1234-1234-12345678912e',
                                            'a1234567-1234-1234-1234-12345678912f'
					)
                GROUP BY stakeholder_identifier
        ) AS a
        INNER JOIN data.stakeholders AS b ON b.stakeholder_identifier = a.stakeholder_identifier AND b.version = a.maxversion
);
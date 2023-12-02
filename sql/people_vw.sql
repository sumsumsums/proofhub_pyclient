create or replace view DEV.TEST_RENDY.PH_PEOPLE_VW(
	ID,
	FIRST_NAME,
	LAST_NAME,
	TITLE,
	EMAIL,
	CREATED_AT,
	UPDATED_AT,
	LAST_ACTIVE
) as
SELECT *
FROM
(
    SELECT
        CAST(JSON_DATA:id AS INTEGER) AS id,
        CAST(JSON_DATA:first_name AS STRING) AS first_name,
        CAST(JSON_DATA:last_name AS STRING) AS last_name,
        CAST(JSON_DATA:title AS STRING) AS title,
        CAST(JSON_DATA:email AS STRING) AS email,
        TRY_TO_TIMESTAMP_NTZ(CAST(JSON_DATA:created_at AS STRING)) AS created_at,
        TRY_TO_TIMESTAMP_NTZ(CAST(JSON_DATA:updated_at AS STRING)) AS updated_at,
        TRY_TO_TIMESTAMP_NTZ(CAST(JSON_DATA:last_active AS STRING)) AS last_active
    FROM PH_PEOPLE_RAW
)
QUALIFY ROW_NUMBER() OVER(PARTITION BY id ORDER BY updated_at DESC) = 1;
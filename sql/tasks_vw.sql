create or replace view DEV.TEST_RENDY.PH_TASKS_VW(
	ID,
	TITLE,
	DESCRIPTION,
	ASSIGNED_0,
	ASSIGNED_1,
	LIST_ID,
	LIST_NAME,
	PROJECT_ID,
	PROJECT_NAME,
	CREATOR_ID,
	CREATED_AT,
	UPDATED_AT,
	COMPLETED_AT,
	COMPLETED,
	COMPLETED_BY,
	STAGE_NAME,
	PERCENT_PROGRESS,
	LABEL_0,
	LABEL_1,
	WORKFLOW_ID,
	WORKFLOW_NAME,
	HISTORY,
	PARENT_ID
) as
SELECT *
FROM (
    SELECT
        CAST(JSON_DATA:id AS INTEGER) AS id,
        CAST(JSON_DATA:title AS STRING) AS title,
        CAST(JSON_DATA:description AS STRING) AS description,
        CAST(JSON_DATA:assigned[0] AS INTEGER) AS assigned_0,
        CAST(JSON_DATA:assigned[1] AS INTEGER) AS assigned_1,
        CAST(JSON_DATA:list.id AS INTEGER) AS list_id,
        CAST(JSON_DATA:list.name AS STRING) AS list_name,
        CAST(JSON_DATA:project.id AS INTEGER) AS project_id,
        CAST(JSON_DATA:project.name AS STRING) AS project_name,
        CAST(JSON_DATA:creator.id AS INTEGER) AS creator_id,
        TRY_TO_TIMESTAMP_NTZ(CAST(JSON_DATA:created_at AS STRING)) AS created_at,
        TRY_TO_TIMESTAMP_NTZ(CAST(JSON_DATA:updated_at AS STRING)) AS updated_at,
        TRY_TO_TIMESTAMP_NTZ(CAST(JSON_DATA:completed_at AS STRING)) AS completed_at,
        CAST(JSON_DATA:completed AS BOOLEAN) AS completed,
        CAST(JSON_DATA:completed_by AS INTEGER) AS completed_by,
        CAST(JSON_DATA:stage.name AS STRING) AS stage_name,
        CAST(JSON_DATA:percent_progress AS FLOAT) AS percent_progress,
        CAST(JSON_DATA:labels[0] AS INTEGER) AS label_0,
        CAST(JSON_DATA:labels[1] AS INTEGER) AS label_1,
        CAST(JSON_DATA:workflow.id AS INTEGER) AS workflow_id,
        CAST(JSON_DATA:workflow.name AS STRING) AS workflow_name,
        CAST(JSON_DATA:task_history AS STRING) AS history,
        CAST(JSON_DATA:parent_id AS INTEGER) AS parent_id
    FROM PH_TASKS_RAW
)
QUALIFY ROW_NUMBER() OVER(PARTITION BY id ORDER BY updated_at DESC) = 1;
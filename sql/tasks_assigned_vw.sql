create or replace view DEV.TEST_RENDY.PH_TASKS_ASSIGNED_VW(
	TASK_ID,
	TITLE,
	ASSIGNED_NAME,
	ASSIGNED_EMAIL,
	LIST_NAME,
	TEAM_NAME,
	PROJECT_NAME,
	STAGE_NAME,
	CREATED_AT,
	UPDATED_AT,
	COMPLETED_AT
) COMMENT='ProofHub Tasks with Assignee Details'
 as
SELECT
    t.id task_id,
    t.title,
    p.first_name || ' ' || p.last_name AS assigned_name,
    p.email AS assigned_email,
    t.list_name,
    CASE
        WHEN LOWER(t.list_name) LIKE '%evermos%' THEN 'SBU Evermos'
        WHEN LOWER(t.list_name) LIKE '%rex%' THEN 'SBU Evermos'
        WHEN LOWER(t.list_name) LIKE '%reseller%' THEN 'SBU Evermos'
        WHEN LOWER(t.list_name) LIKE '%everpro%' THEN 'SBU Everpro'
        WHEN LOWER(t.list_name) LIKE '%finance%' THEN 'Corporate'
        WHEN LOWER(t.list_name) LIKE '%corporate%' THEN 'Corporate'
        WHEN LOWER(t.list_name) LIKE '%digital%' THEN 'Digital'
        WHEN LOWER(t.list_name) LIKE '%digi%' THEN 'Digital'
        WHEN LOWER(t.list_name) LIKE '%logistic%' THEN 'Logistic'
        WHEN LOWER(t.list_name) LIKE '%marketing%' THEN 'Marketing'
        WHEN LOWER(t.list_name) LIKE '%data engineering%' THEN 'Data Engineering'
        WHEN LOWER(t.list_name) LIKE '%tech%' THEN 'Data Engineering'
        WHEN LOWER(t.list_name) LIKE '%bi%' THEN 'BI'
        WHEN LOWER(t.list_name) LIKE '%crm%' THEN 'CRM'
        WHEN LOWER(t.list_name) LIKE '%cbp%' THEN 'CBP'
        WHEN LOWER(t.list_name) LIKE '%ds%' THEN 'DS'
        WHEN LOWER(t.list_name) LIKE '%customer%' THEN 'Customer Platform'
        ELSE t.list_name
    END AS team_name,
    t.project_name,
    t.stage_name,
    t.created_at,
    t.updated_at,
    t.completed_at
FROM DEV.TEST_RENDY.PH_TASKS_VW t
    LEFT JOIN DEV.TEST_RENDY.PH_PEOPLE_VW p
        ON t.assigned_0 = p.id;
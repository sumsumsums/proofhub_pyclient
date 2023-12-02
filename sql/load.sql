CREATE OR REPLACE STAGE dev_rendy_stage file_format = (type = json);
PUT file:///Users/evermos/repo/proofhub_pyclient/tasks.json @dev_rendy_stage;
CREATE OR REPLACE TABLE PH_TASKS_RAW (json_data VARIANT );
COPY INTO PH_TASKS_RAW FROM @dev_rendy_stage/tasks.json.gz;

PUT file:///Users/evermos/repo/proofhub_pyclient/output/people/people.json @dev_rendy_stage;
CREATE OR REPLACE TABLE PH_PEOPLE_RAW (json_data VARIANT );
COPY INTO PH_PEOPLE_RAW FROM @dev_rendy_stage/people.json.gz;
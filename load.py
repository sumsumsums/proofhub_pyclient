import os

import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    role=os.getenv('SNOWFLAKE_ROLE'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

results = conn.cursor().execute('PUT file:///Users/evermos/repo/proofhub_pyclient/tasks.json @dev_rendy_stage OVERWRITE = TRUE')
for result in results:
    print(result)

results = conn.cursor().execute('COPY INTO PH_TASKS_RAW FROM @dev_rendy_stage/tasks.json.gz')
for result in results:
    print(result)

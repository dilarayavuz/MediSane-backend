from os import environ as env

## RDS MySQL constants
# TODO: turn these into environment variables
sql_host = env.get("DB_ENDPOINT")
sql_port = 3306
user = env.get("DB_USERNAME")
pw = env.get("DB_PASSWORD")

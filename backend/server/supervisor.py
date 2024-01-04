from backend.sql.supervisor import get_patients_sql
from backend.callers.db import execute_parameterized_query, insert_into_table, execute_query

class Supervisor:
    profile_id: str

    def __init__(self, profile_id):
        self.profile_id = profile_id


    def get_patients(self):
        from backend import engine
        result = execute_parameterized_query(query=get_patients_sql, engine=engine, supervisor_id=self.profile_id)

        return result

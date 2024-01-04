from datetime import datetime, time
from typing import Optional, List

from pydantic import BaseModel

from backend.callers.db import execute_query
from backend.server.login import fetch_exists_result
from backend.sql.medicine import clash_check_sql


class Medicine(BaseModel):

    medicine_name: str
    frequency: int
    start_dates: List[datetime]

    dose_amount: Optional[int]
    usage_description: Optional[str]
    has_notif: Optional[bool] = False
    remaining_amount: Optional[int]
    end_date: Optional[datetime]

    def medicine_exists(self):
        from backend import engine
        result = execute_query(query=f"SELECT EXISTS(SELECT * FROM medicine WHERE name=\'{self.medicine_name}\') ",
                               engine=engine)

        if not result or result == -1:
            return -1


        return fetch_exists_result(result)

    @staticmethod
    def check_clash(medicine_list: list):
        from backend import engine

        medicine_list_str = ", ".join(f"'{s}'" for s in medicine_list)
        result = execute_query(query=clash_check_sql.format(medicine_list_str=medicine_list_str),
                               engine=engine)

        print(result)

        return [(row['medicine_1'], row['medicine_2'], row['clash_level']) for row in result]
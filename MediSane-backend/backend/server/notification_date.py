
import json
import requests
from pydantic import BaseModel
from backend.callers.db import execute_query
from os import environ as env

class Notification_Date(BaseModel):
    id: int

    @staticmethod
    def get_medicine_info(id):
        from backend import engine
        result = execute_query(query=f"SELECT medicine_name, start_date FROM dosage_time WHERE patient_id=\'{id}\'",
                               engine=engine)

        return result

    @staticmethod
    def send_notif(payload):
        from backend import engine
        url = 'https://fcm.googleapis.com/fcm/send'
        auth_key = env.get("FCM_AUTH_KEY")
        #private hale getirmemiz lazım burayı
        headers = {"Content-Type": "application/json",
                   "Authorization": f"key={auth_key}"
                   }

        requests.post(url, data=json.dumps(payload), headers=headers)
from backend.validations import Notification
from backend.server import notification_date

from fastapi import APIRouter
from os import environ as env

class NotificationController:
    router = APIRouter()

    @staticmethod
    @router.post("/send-push-notification")
    async def send_push_notification(payload: Notification):
        query_res = notification_date.Notification_Date.get_medicine_info(payload.patient_id)
        #fcm token'ı cihazdan çekmemiz lazım burası değişicek
        fcm_token = env.get("FCM_TOKEN")

        if len(query_res) != 0:
            for element in query_res:
                start_date = element.get("start_date")
                name = element.get("medicine_name")

                """
                FCM Data Payload
                { 
                    "to": "/topics/discount-offers", 
                    "priority": "high",
                    "data" : {
                      "title" : "TITLE_HERE",
                      "message" : "MESSAGE_HERE",
                      "isScheduled" : "true",
                      "scheduledTime" : "2019-12-13 09:41:00"
                    }
                }
                """

                start_date = "2023-12-21 12:27:00"

                new_payload = {
                    "data": {
                        "title": "CANA çalış pls 12.27 pls",
                        "body": "take your " + name + "!!!",
                        "isScheduled": True if start_date is not None else False,
                        "scheduledTime": start_date if start_date is not None else None
                    },
                    "to": fcm_token
                }
                print("new payload")
                print(new_payload)

                #scheduling implementation is going to be added to android/ios project
                notification_date.Notification_Date.send_notif(new_payload)

        return 1
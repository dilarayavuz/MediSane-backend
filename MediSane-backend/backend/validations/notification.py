from pydantic import BaseModel


class Notification(BaseModel):
    patient_id: int
    # might change to user token


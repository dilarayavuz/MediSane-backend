from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class MedicinePatient(BaseModel):
    medicine_name:      str
    patient_id:         int
    frequency:          int
    start_dates:        List[datetime]

    dose_amount:        Optional[int] = None
    usage_description:  Optional[str] = None
    has_notif:          Optional[bool] = False
    remaining_amount:   Optional[int] = None
    end_date:           Optional[datetime] = None

    token:              str

from pydantic import BaseModel
class MedicineReport(BaseModel):
    patient_id: int
    medicine_name: str
    label: bool
    hour_of_dose: str
    is_update: bool

    token: str


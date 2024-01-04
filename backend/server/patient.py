from backend.validations import MedicinePatient
from backend.server.medicine import Medicine
from backend.callers.db import execute_parameterized_query, insert_into_table, execute_query, update_table
from backend.sql.medicine import get_medicines_sql
from fastapi import status, HTTPException


class Patient:
    profile_id: int

    def __init__(self, profile_id):

        self.profile_id = profile_id




    def add_medicine(self,  medicine: Medicine):
        from backend import engine
        print(f'cols:{[k for k,v in medicine.dict().items() if v is not None and k != "start_dates"]}\n'
              f'vals:{[v for k,v in medicine.dict().items() if v is not None and k != "start_dates"]}')

        exists = medicine.medicine_exists()
        if not exists:
            res = insert_into_table(table="medicine",
                                    columns=["name"],
                                    values=[medicine.medicine_name],
                                    engine=engine)
            print(f"Medicine {medicine.medicine_name} was not found in the medicine table.")
            if res != -1:
                print("A new medicine record with this name was added.")
            else:
                print("Error during inserting new medicine to medicine table.")
                return -1, -1

        elif exists == -1:
            print("Error in medicine check query execution.")
            return -1, -1

        elif exists:
            print("Medicine already in database")

        medicine_added = insert_into_table(table="patient_uses_medicine",
                                           columns=["patient_id"]+[k for k,v in medicine.dict().items() if v is not None and k != "start_dates"],
                                           values=[self.profile_id]+[v for k,v in medicine.dict().items() if v is not None and k != "start_dates"],
                                           engine=engine)

        dates_added = ""
        for date in medicine.start_dates:
            dates_added = insert_into_table(table="dosage_time",
                                            columns=["patient_id", "medicine_name", "start_date"],
                                            values=[self.profile_id, medicine.medicine_name, date],
                                            engine=engine)

        return medicine_added, dates_added

    def get_all_medicines(self):
        from backend import engine
        result = execute_query(query=get_medicines_sql.format(profile_id=self.profile_id),
                               engine=engine)

        if result == -1:
            print("Failed to get patients medicines, possibly due to profile being a supervisor")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to get patients medicines",
            )

        all_medicines = [med["medicine_name"] for med in result]
        if all_medicines:
            clashes = Medicine.check_clash(all_medicines)
        else:
            clashes = []

        return result, clashes

    def add_medicine_report(self, medicine_report, is_update):
        from backend import engine
        if not is_update:
            report_put = insert_into_table(table="medicine_report",
                                             values=[v for k, v in medicine_report.items()],
                                             columns=[k for k in medicine_report.keys()],
                                             engine=engine)
        else:  # TODO: add an update check
            report_put = update_table(table="medicine_report",
                                      values=[medicine_report["label"]],
                                      columns=["label"],
                                      where={k: v for k, v in medicine_report.items() if k != "label"},
                                      engine=engine)

        return report_put

    def get_medicine_report(self):
        from backend import engine
        result = execute_query(query=f"SELECT * FROM medicine_report WHERE patient_id={self.profile_id} ORDER BY hour_of_dose DESC",
                               engine=engine)

        return result
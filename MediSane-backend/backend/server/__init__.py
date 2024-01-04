from backend.server.endpoint import EndPoint
from backend.controllers.login import LoginController
from backend.controllers.notifications import NotificationController
from backend.controllers.signup import SignupController
from backend.controllers.patient import ScheduleMedicineController, AllMedicinesController, AddMedicineReportController, GetMedicineReportController
from backend.controllers.supervisor import GetPatientsController
from backend.controllers.profile import AddProfileController, DeleteProfileController

login_ep = EndPoint(router=LoginController.router, prefix="/post")
send_notification_ep = EndPoint(router=NotificationController.router, prefix="/post")
signup_ep = EndPoint(router=SignupController.router, prefix="/put")
schedule_medicine_ep = EndPoint(router=ScheduleMedicineController.router, prefix="/put")
all_med_ep = EndPoint(router=AllMedicinesController.router, prefix="/post")
get_patients_ep = EndPoint(router=GetPatientsController.router, prefix="/post")
add_medicine_report_ep = EndPoint(router=AddMedicineReportController.router, prefix="/put")
get_medicine_report_ep = EndPoint(router=GetMedicineReportController.router, prefix="/post")
add_profiles_ep = EndPoint(router=AddProfileController.router, prefix="/put")
delete_profiles_ep = EndPoint(router=DeleteProfileController.router, prefix="/delete")


__all__ = ["login_ep", "schedule_medicine_ep", "all_med_ep", "signup_ep",
           "get_patients_ep", "add_medicine_report_ep", "get_medicine_report_ep",
           "add_profiles_ep", "delete_profiles_ep", "send_notification_ep"]
from backend.validations import Profile


def patients_check(patient_id: int, profiles: [Profile]):
    for profile in profiles:
        if profile["type"] == "supervisor":
            return True
        else:
            if profile["profileId"] == patient_id:
                return True

    return False


def supervisor_check(supervisor_id: int, profiles: [Profile]):
    for profile in profiles:
        if profile["type"] == "supervisor" and profile["profileId"] == supervisor_id:
            return True

    return False

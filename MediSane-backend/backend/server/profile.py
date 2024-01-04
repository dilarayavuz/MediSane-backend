from backend.callers.db import execute_query, insert_into_table, delete_from_table

def add_profile(account_id: int, profile_name: str, type: str):
    from backend import engine

    profile_created = insert_into_table(table="profile",
                                       columns=["account_id", "profile_name"],
                                       values=[account_id, profile_name],
                                       engine=engine)

    profile_id = get_profile_id(account_id, profile_name)

    type_created = insert_into_table(table=type,
                                     columns=["profile_id"],
                                     values=[profile_id],
                                     engine=engine)

    return profile_created and type_created

def get_profile_id(account_id: int, profile_name: str):
    from backend import engine

    res = execute_query(query=f"SELECT profile_id FROM profile WHERE account_id='{account_id}' AND profile_name='{profile_name}'",
                        engine=engine)

    return res[0]["profile_id"]

def delete_profile(profile_id: int):
    from backend import engine

    res = delete_from_table(table='profile',
                            where={'profile_id': profile_id},
                            engine=engine)

    return bool(res)

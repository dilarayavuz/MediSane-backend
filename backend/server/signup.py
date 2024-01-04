import uuid
from hashlib import sha256


from backend.callers.db import insert_into_table


def signup(username: str, password: str):
    from backend import engine
    salt = str(uuid.uuid4())
    hashed_pw = sha256((password+salt).encode('utf-8')).hexdigest()
    print(f"Signup.\nusername: {username} \npw: {password}\nhashed_pw: {hashed_pw}\nsalt: {salt}")
    res = insert_into_table(table="account",
                            columns=["username", "password", "salt"],
                            values=[username, hashed_pw, salt],
                            engine=engine)

    if res != -1:
        print("account created")
    else:
        print("error during account creation")

    return res

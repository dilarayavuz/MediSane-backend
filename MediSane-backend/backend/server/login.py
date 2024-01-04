from backend.callers.db import execute_parameterized_query
from backend.sql.login import login_sql, profiles_sql, profiles_from_id_sql, salt_sql, account_sql
from backend.utils.db_utils import fetch_exists_result
from backend.validations import Account, LoginInfo, Profile
from datetime import datetime, timedelta
import jwt
from backend.constants.login_constants import secret_key, algorithm, access_token_expiration
from fastapi import status, HTTPException
import uuid
from hashlib import sha256


def check_user(credentials: LoginInfo):
    from backend import engine

    salt = execute_parameterized_query(query=salt_sql, engine=engine, username=credentials.username)[0].get('salt')
    print(f"salt = {salt}")
    print(f"pass = {credentials.password}")
    hashed_pw = sha256((credentials.password + salt).encode('utf-8')).hexdigest()
    print(f"hashed pw = {hashed_pw}")

    result = execute_parameterized_query(query=login_sql,
                                         engine=engine, username=credentials.username, password=hashed_pw)

    if not result or result == -1:
        return False

    return fetch_exists_result(result)

def get_account_id(username: str):  #Dilara
    from backend import engine
    result = execute_parameterized_query(query=account_sql,
                                         engine=engine, username=username)

    return result



def get_account_profiles(username: str):  #Bartu
    from backend import engine
    result = execute_parameterized_query(query=profiles_sql,
                                         engine=engine, username=username)

    return result

def get_account_profiles_from_id(account_id: int):  #Bartu
    from backend import engine
    result = execute_parameterized_query(query=profiles_from_id_sql,
                                         engine=engine, account_id=account_id)

    return result


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_user(token: str) -> (int, [Profile]):
    from backend import engine

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        accountID: str = decoded_token.get("AccountID")
        profiles: [Profile] = decoded_token.get("profiles")
        if accountID is None:
            raise credentials_exception
    except Exception as e:
        print(e)
        raise credentials_exception
    if profiles is None:
        raise credentials_exception
    return accountID, profiles

from datetime import datetime

import sqlalchemy
from sqlalchemy.exc import ResourceClosedError

# It could be the case that mysql fails to import even when installed.
# In that case, uncomment the below lines and fill the absolute
# path with the path to your pymysql package.

# import sys
# sys.path.append("{path to your pymysql}")

import pymysql
import paramiko
from sqlalchemy import create_engine
from backend.constants import db_constants
from backend.sql.general_purpose import insert_sql
import base64


def execute_parameterized_query(query: str, engine, **kwargs):
    try:
        with engine.connect() as connection:
            print(f"Connection established:\n {connection}")
            print(f"\nExecuting query:\n {query}\n")
            result_proxy = connection.execute(sqlalchemy.text(query), kwargs)
            columns = result_proxy.keys()
            all_rows = []
            for row in result_proxy:
                all_rows.append(dict((column, value) for column, value in zip(columns, row)))

    except Exception as e:
        print(e, flush=True)
        return -1

    return all_rows

def execute_query(query: str, engine, commit=False):
    try:
        with engine.connect() as connection:
            print(f"Connection established:\n {connection}")
            print(f"\nExecuting query:\n {query}\n")
            result_proxy = connection.execute(sqlalchemy.text(query))
            columns = result_proxy.keys()
            all_rows = []
            for row in result_proxy:
                all_rows.append(dict((column, value) for column, value in zip(columns, row)))
            if commit:
                connection.commit()

    except Exception as e:
        if isinstance(e, ResourceClosedError):
            print("Insertion successful.")
            return 1
        else:
            print(e, flush=True)
            return -1

    return all_rows


def create_db_engine():
    try:
        engine = create_engine(
            f'mysql+pymysql://{db_constants.user}:{db_constants.pw}@{db_constants.sql_host}:3306/app?autocommit=true')

    except Exception as e:
        print(e, flush=True)
        return -1

    return engine





def insert_into_table(table: str, columns: [str], values: list, engine):
    assert len(columns) == len(values)
    columns_str = ', '.join(columns)

    values = list(map(lambda x: f"\'{x}\'" if isinstance(x, str) or isinstance(x, datetime)
    else x, values))
    values = list(map(lambda x: str(x), values))
    values_str = ', '.join(values)

    res = execute_query(query=f'INSERT INTO {table}({columns_str}) VALUES ({values_str})',
                        engine=engine, commit=True)
    return int(res)

def update_table(table: str, columns: [str], values: list, where: dict, engine):
    assert len(columns) == len(values)

    values = list(map(lambda x: f"\'{x}\'" if isinstance(x, str) or isinstance(x, datetime)
    else x, values))
    values = list(map(lambda x: str(x), values))
    print(values)
    set_str = ', '.join(f'{key}={value}' for key, value in zip(columns, values))

    where_values, where_keys = [v for k, v in where.items()], [k for k, v in where.items()]
    where_values = list(map(lambda x: f"\'{x}\'" if isinstance(x, str) or isinstance(x, datetime)
    else x, where_values))
    where_values = list(map(lambda x: str(x), where_values))

    where_str = ' and '.join(f'{key}={value}' for key, value in zip(where_keys, where_values))

    res = execute_query(query=f'UPDATE {table} SET {set_str} WHERE {where_str}',
                        engine=engine, commit=True)

    return int(res)

def delete_from_table(table: str, where: dict, engine):

    where_values, where_keys = [v for k, v in where.items()], [k for k, v in where.items()]
    where_values = list(map(lambda x: f"\'{x}\'" if isinstance(x, str) or isinstance(x, datetime)
    else x, where_values))
    where_values = list(map(lambda x: str(x), where_values))

    where_str = ' and '.join(f'{key}={value}' for key, value in zip(where_keys, where_values))

    res = execute_query(query=f'DELETE FROM {table} WHERE {where_str}',
                        engine=engine, commit=True)

    return int(res)


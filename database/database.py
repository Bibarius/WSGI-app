import sqlite3
import os

def dir_change(func):

    def wrapper(arg):

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        value = func(arg)
        os.chdir('../')

        return value
    
    return wrapper


@dir_change
def find_session(session_id) -> bool:

    database_name = 'users.db'

    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    cursor.execute("""
                    SELECT sessionid
                    FROM users
               """)

    
    for row in cursor.fetchall():
        if float(session_id) in row:
            return True
    
    return False

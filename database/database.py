import sqlite3
import os

def dir_change(foo):
    def wrapper(*args):

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        value = foo(*args)
        os.chdir('../')
        return value
        
    return wrapper

@dir_change
def add_session(email, password, session_id):
    database_name = 'users.db'
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    cursor.execute("""
                    UPDATE users 
                    SET sessionid = :sesion_id
                    WHERE email == :email and password = :password
               """, {'sesion_id': session_id, 'email': email, 'password': password})

    con.commit()
    con.close()

@dir_change
def delete_session(session_id):
    database_name = 'users.db'
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    cursor.execute("""
                    UPDATE users 
                    SET sessionid = NULL
                    WHERE sessionid == :session_id
               """, {'session_id': session_id})
    
    con.commit()
    con.close()

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

@dir_change
def add_user(email, password):
    database_name = 'users.db'
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    cursor.execute("""
                    INSERT INTO users (email, password)
                    VALUES (?, ?)
                   """, (email, password))

    con.commit()
    con.close()


@dir_change
def find_user(email, password):
    database_name = 'users.db'
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    cursor.execute("""
                    SELECT email, password
                    FROM users
                  """)

    for row in cursor.fetchall():
        if (email, password) == row:
            con.close()
            return True

    con.close()
    return False


delete_session(3343959872)
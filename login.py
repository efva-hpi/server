import bcrypt
from Datenbankverbindung import sql
from psycopg2 import Error as psycopg2Error


def hash_password(password: str) -> bytes:
    """
    Takes a password string and returns a hash of it.
    """
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)


def register(username: str, password: str, email: str) -> bool:
    try:
        return sql.add_spieler(username, hash_password(password).decode(), email)
    except psycopg2Error as e:
        print(f"Error while registering: {e.pgerror}")
        raise e


def login(username: str, password: str) -> bool:
    try:
        return check_password(password, sql.get_password(username))
    except psycopg2Error as e:
        print(f"Error during login: {e.pgerror}")
        raise e


def change_password(username: str, old_pw: str, new_pw: str) -> bool:
    if login(username, old_pw):
        result = sql.execute_update_query("UPDATE Spieler SET passwort= %s WHERE benutzername = %s OR email = %s;", (new_pw, username, username))
        if result:
            return True #hat geklappt
        else:
            return False #das war mies
    else:
        raise ValueError("Incorrect current password")
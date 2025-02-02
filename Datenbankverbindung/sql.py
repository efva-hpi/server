import psycopg2
from get_docker_secret import get_docker_secret
import os

db_pw = get_docker_secret("PG_PW", default = "efva-pw")
if db_pw != "efva-pw":
    with open(db_pw, "r") as f:
        db_pw = f.read().strip()

db_params = {
    'dbname': 'efva-db',
    'user': 'efva',
    'password': db_pw,
    'host': 'db'
}

def connect() -> psycopg2.extensions.connection:
    try:
        return psycopg2.connect(**db_params)
    except psycopg2.Error as e:
        print(f"Error while connecting: {e.pgerror}")
        raise e

def execute_select_query(query, data):
    try:
        # Verbindung zur Datenbank herstellen
        with connect() as conn:
            with conn.cursor() as cur:
                # SQL-Abfrage ausführen
                cur.execute(query, data)
                # Alle Ergebnisse abrufen
                results = cur.fetchall()

        return results

    except psycopg2.Error as e:
        print(f"Error while executing a select query: {e.pgerror}")
    finally:
        # Cursor und Verbindung schließen
        if conn:
            if cur:
                cur.close()
            conn.close()

def execute_select_one_query(query, data):
    try:
        # Verbindung zur Datenbank herstellen
        with connect() as conn:
            with conn.cursor() as cur:
                # SQL-Abfrage ausführen
                cur.execute(query, data)
                # Alle Ergebnisse abrufen
                result = cur.fetchone()

        return result

    except psycopg2.Error as e:
        print(f"Error while executing a select query: {e.pgerror}")
    finally:
        # Cursor und Verbindung schließen
        if conn: 
            if cur:
                cur.close()
            conn.close()

def execute_insert_query(query, data) -> bool:
    result = None
    query = query[:-1] + " RETURNING *;"
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, data)
                result = cur.fetchone()

        return bool(result)
    except psycopg2.Error as e:
        print(f"Error while inserting: {e.pgerror}")
        raise e

def execute_update_query(query, data) -> int:
    updated_rows = 0
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, data)
                updated_rows = cur.rowcount

        return updated_rows
    except psycopg2.Error as e:
        print(f"Error while updating: {e.pgerror}")
        raise e

def get_password(anmeldename: str) -> bytes:
    try:
        result = execute_select_one_query("SELECT passwort FROM spieler WHERE benutzername = %s OR email = %s;", (anmeldename,anmeldename))
        if not result:
            raise ValueError(f"No user associated with email or username {anmeldename}")
        return result[0]

    except psycopg2.Error as e:
        print(f"Error while retrieving password: {e.pgerror}")
        raise e

def add_spieler(anmeldename: str, passwort: str, email: str) -> bool:
    try:
        result = execute_insert_query("INSERT INTO Spieler VALUES (%s, %s, %s);", (anmeldename, passwort, email))
        return result
    except psycopg2.Error as e:
        print(f"Error while adding player: {e.pgerror}")
        raise e

def neues_spiel(fragenanzahl):
    result = execute_insert_query("INSERT INTO Spiel (fragenanzahl) VALUES (%s);", fragenanzahl)
    return result

def neue_statistik(benutzername, spielID, punktzahl, platzierung):
    result = execute_insert_query("INSERT INTO Statistik VALUES (%s, %s, %s, %s);", (benutzername, spielID, punktzahl, platzierung))

    return result

def anzahl_spiele(benutzername):
    result = execute_select_query("SELECT COUNT(spielerbenutzername) FROM Statistik WHERE spielerbenutzername = %s;" ,(benutzername, ))

    return result[0][0]

def anzahl_gewonnene_spiele(benutzername):
    result = execute_select_query("SELECT COUNT(spielerbenutzername) FROM Statistik WHERE spielerbenutzername = %s AND platzierung = 1;", (benutzername, ))

    return result[0][0]

def punkte_pro_frage(benutzername):
    result = execute_select_query("SELECT CAST(SUM(Statistik.punktzahl) AS float)/CAST(SUM(Spiel.fragenanzahl) AS float) FROM Statistik INNER JOIN Spiel ON Statistik.spielID=Spiel.ID WHERE Statistik.spielerbenutzername = %s", (benutzername, ))

    return result

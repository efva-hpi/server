import psycopg2

db_params = {
    'dbname': 'efva',
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def connect():
    try:
        with psycopg2.connect(**db_params) as conn:
            #print("Connected to PostgreSQL")
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def execute_select_query(query):
    try:
        # Verbindung zur Datenbank herstellen
        conn = connect()
        cur = conn.cursor()
        # SQL-Abfrage ausführen
        cur.execute(query)
                    # Alle Ergebnisse abrufen
        results = cur.fetchall()

        return results

    except Exception as e:
        print(f"Fehler: {e}")
        return None
    finally:
        # Cursor und Verbindung schließen
        if cur:
            cur.close()
        if conn:
            conn.close()

def execute_insert_query(query):
    result = None
    query = query[:-1] + " RETURNING *;"
    try:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchone()
            if rows:
                result = rows[0]

            conn.commit()

        return result
    except (Exception, psycopg2.DatabaseError) as error:
        return error

def execute_update_query(query):
    updated_rows = 0
    try:
        conn = connect()
        with conn.cursor() as cur:

            cur.execute(query)
            updated_rows = cur.rowcount

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        return updated_rows


def anmelden(anmeldename, passwort):
    result = execute_select_query(f"SELECT passwort FROM spieler WHERE benutzername = \'{anmeldename}\' or email = \'{anmeldename}\';")
    if len(result) == 0:
        raise ValueError(f"Es existiert kein Konto mit dem Benutzernamen oder der E-Mail: \"{anmeldename}\"")
    if result[0][0] == passwort:
        return True         #passwort richtig
    else:
        return False        #passwort falsch

def addSpieler(benutzername, passwort, email):
    result = execute_insert_query(f"INSERT INTO Spieler VALUES (\'{benutzername}\', \'{passwort}\', \'{email}\');")
    if result == benutzername:
        return True     #wurde erstellt
    else:
        return result   #gibt Fehler zurück

def changePS(anmeldename, altesPasswort, neuesPasswort):
    if anmelden(anmeldename, altesPasswort):
        result = execute_update_query(f"UPDATE Spieler SET passwort= \'{neuesPasswort}\' WHERE benutzername = \'{anmeldename}\' OR email = \'{anmeldename}\';")
        if result:
            return True #hat geklappt
        else:
            return False #das war mies
    else:
        raise ValueError("Falsches Passwort")

def neuesSpiel(fragenanzahl):
    result = execute_insert_query(f"INSERT INTO Spiel (fragenanzahl) VALUES ({fragenanzahl});")
    return result

def neueStatistik(benutzername, spielID, punktzahl, platzierung):
    result = execute_insert_query(f"INSERT INTO Statistik VALUES (\'{benutzername}\', {spielID}, {punktzahl}, {platzierung});")

    return result

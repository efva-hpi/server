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

def execute_select_query(query, data):
    try:
        # Verbindung zur Datenbank herstellen
        conn = connect()
        cur = conn.cursor()
        # SQL-Abfrage ausführen
        cur.execute(query, data)
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

def execute_insert_query(query, data):
    result = None
    query = query[:-1] + " RETURNING *;"
    try:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute(query, data)
            rows = cur.fetchone()
            if rows:
                result = rows[0]

            conn.commit()

        return result
    except (Exception, psycopg2.DatabaseError) as error:
        return error

def execute_update_query(query, data):
    updated_rows = 0
    try:
        conn = connect()
        with conn.cursor() as cur:

            cur.execute(query, data)
            updated_rows = cur.rowcount

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        return updated_rows


def anmelden(anmeldename, passwort):
    result = execute_select_query("SELECT passwort FROM spieler WHERE benutzername = %s or email = %s;", (anmeldename, anmeldename))
    if len(result) == 0:
        raise ValueError(f"Es existiert kein Konto mit dem Benutzernamen oder der E-Mail: \"{anmeldename}\"")
    if result[0][0] == passwort:
        return True         #passwort richtig
    else:
        return False        #passwort falsch

def addSpieler(benutzername, passwort, email):
    result = execute_insert_query("INSERT INTO Spieler VALUES (%s, %s, %s);", (benutzername, passwort, email))
    if result == benutzername:
        return True     #wurde erstellt
    else:
        return result   #gibt Fehler zurück

def changePS(anmeldename, altesPasswort, neuesPasswort):
    if anmelden(anmeldename, altesPasswort):
        result = execute_update_query("UPDATE Spieler SET passwort= %s WHERE benutzername = %s OR email = %s;", (neuesPasswort, anmeldename, anmeldename))
        if result:
            return True #hat geklappt
        else:
            return False #das war mies
    else:
        raise ValueError("Falsches Passwort")

def neuesSpiel(fragenanzahl):
    result = execute_insert_query("INSERT INTO Spiel (fragenanzahl) VALUES (%s);", (fragenanzahl,))
    return result

def neueStatistik(benutzername, spielID, punktzahl, platzierung):
    result = execute_insert_query("INSERT INTO Statistik VALUES (%s, %s, %s, %s);", (benutzername, spielID, punktzahl, platzierung))

    return result

def anzahlSpiele(benutzername):
    result = execute_select_query("SELECT COUNT(spielerbenutzername) FROM Statistik WHERE spielerbenutzername = %s;" ,(benutzername, ))

    return result[0][0]

def anzahlgewonneneSpiel(benutzername):
    result = execute_select_query("SELECT COUNT(spielerbenutzername) FROM Statistik WHERE spielerbenutzername = %s AND platzierung = 1;", (benutzername, ))

    return result[0][0]

def punkteproFrage(benutzername):
    result = execute_select_query("SELECT CAST(SUM(Statistik.punktzahl) AS float)/CAST(SUM(Spiel.fragenanzahl) AS float) FROM Statistik INNER JOIN Spiel ON Statistik.spielID=Spiel.ID WHERE Statistik.spielerbenutzername = %s", (benutzername, ))

    return result

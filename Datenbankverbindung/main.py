import sql

jsAddSpieler = {
    "case": "addSpieler",
    "anmeldename": "horst",
    "email": "herbricht@gmail.com",
    "passwort": "herbert"
}

jsAnmelden = {
    "case": "anmelden",
    "anmeldename": "horst",
    "passwort": "herbert"
}

jsChPs = {
    "case": "changePS",
    "anmeldename": "horst",
    "passwort": "herbert",
    "neuespasswort": "grönemeyer"
}

jsSpiel = {
    "case": "neuesSpiel",
    "anzahlFragen": 20
}

jsStatistik = {
    "case": "neueStatistik",
    "anmeldename": "horst",
    "spielID": 4,
    "punktzahl": 20,
    "platzierung": 1
}

def main(json):
    match json["case"]:
        case "anmelden":
            return sql.anmelden(json["anmeldename"], json["passwort"])
        case "changePS":
            return sql.changePS(json["anmeldename"], json["passwort"], json["neuespasswort"])
        case "addSpieler":
            return sql.addSpieler(json["anmeldename"], json["passwort"], json["email"])
        case "neuesSpiel":
            return sql.neuesSpiel(json["anzahlFragen"])
        case "neueStatistik":
            return sql.neueStatistik(json["anmeldename"], json["spielID"], json["punktzahl"], json["platzierung"])
        case _:
            return "Bist du dumm?"
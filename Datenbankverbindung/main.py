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


def main(anfrage):
    match anfrage["case"]:
        case "anmelden":
            return sql.anmelden(anfrage["anmeldename"], anfrage["passwort"])
        case "changePS":
            return sql.changePS(anfrage["anmeldename"], anfrage["passwort"], anfrage["neuespasswort"])
        case "addSpieler":
            return sql.addSpieler(anfrage["anmeldename"], anfrage["passwort"], anfrage["email"])
        case "neuesSpiel":
            return sql.neuesSpiel(anfrage["anzahlFragen"])
        case "neueStatistik":
            return sql.neueStatistik(anfrage["anmeldename"], anfrage["spielID"], anfrage["punktzahl"], anfrage["platzierung"])
        case _:
            return "Bist du dumm?"
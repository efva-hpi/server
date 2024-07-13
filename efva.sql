CREATE DATABASE efva;

CREATE TABLE Spieler (
    benutzername varchar(255) PRIMARY KEY,
    passwort varchar(255) NOT NULL,
    email varchar(255) NOT NULL UNIQUE
);

CREATE TABLE Spiel (
    ID SERIAL PRIMARY KEY,
    fragenanzahl int NOT NULL
);

CREATE TABLE Statistik (
    spielerbenutzername varchar(255),
    spielID int,
    punktzahl int NOT NULL,
    platzierung int NOT NULL,

    PRIMARY KEY(spielerbenutzername, spielID),
    FOREIGN KEY (spielerbenutzername) REFERENCES Spieler(benutzername), 
    FOREIGN KEY (spielID) REFERENCES Spiel(ID)
);
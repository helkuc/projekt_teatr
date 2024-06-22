# import mysql
# import mysql.connector
# config={"user":"root","password":"###","host":"localhost","database":"teatr"}
# connect = mysql.connector.connect(**config)

## tworzenie bazy teatr
# zapytanie = "create database teatr"
# cursor.execute(zapytanie)

# # tworzenie tabeli listaMiejsc
# zapytanie ="""create table listaMiejsc (
# 	numer int auto_increment primary key,
#
#     dostepne boolean,
#     cena float not null,
#     dodatkowaOplata float,
#     udogodnienia varchar(250),
#     typ varchar(100) not null

# );"""
# cursor.execute(zapytanie)

# # tworzenie tabeli rezerwacje
# zapytanie ="""create table rezerwacje (
# 	idRezerwacji int auto_increment primary key,
#     dataRezerwacji datetime,
#     status varchar(50),
#     idKlienta int,
#     numerMiejsca int,
#     typ varchar(100)
# );"""
# cursor.execute(zapytanie)

# tworzenie tabeli rezerwacje
# zapytanie ="""create table listaKlientow (
# 	idKlienta int auto_increment primary key,
#     imie varchar(100),
#     nazwisko varchar(250)
# );"""
# cursor.execute(zapytanie)


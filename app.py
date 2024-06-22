import mysql
import mysql.connector
from datetime import datetime
import tkinter
from tkinter import messagebox
from functools import partial

#połączanie z bazą danych
def connectToDatabase ():
    config = {"user": "root", "password": "Rozilka89!!!", "host": "localhost", "database": "teatr"}
    global connect
    connect = mysql.connector.connect(**config)
    global cursor
    cursor = connect.cursor()

# ogólna klasa miejsca
class MiejsceTeatralne:
    def __init__(self,numer,dostepne,cena):
        self.numer = numer
        self.dostepne = dostepne
        self.cena = cena

# klasa zwykłe miejsca
class MiejsceZwykle(MiejsceTeatralne):
    def __init__(self,numer,dostepne,cena):
        MiejsceTeatralne.__init__(self,numer,dostepne,cena)

    def __str__(self):
        return f"Numer miejsca: {self.numer}, dostępność: {self.dostepne}, cena biletu: {self.cena}"

    def listaParametrow(self):
        return (self.numer,"zwykłe",self.dostepne,self.cena)

# klasa VIP miejsca
class MiejsceVIP(MiejsceTeatralne):
    def __init__(self,numer,dostepne,cena,dodatkowaOplata):
        MiejsceTeatralne.__init__(self,numer,dostepne,cena)
        self.dodatkowaOplata = dodatkowaOplata

    def __str__(self):
        return f"Numer miejsca: {self.numer}, dostępność: {self.dostepne}, cena biletu: {self.cena}, dodatkowa opłata  {self.dodatkowaOplata}"

# klasa miejsca dla niepełnosprawnych
class MiejsceDlaNiepelnosprawnych(MiejsceTeatralne):
    def __init__(self,numer,dostepne,cena,udogodnienia):
        MiejsceTeatralne.__init__(self,numer,dostepne,cena)
        self.udogodnienia = udogodnienia

    def __str__(self):
        return f"Numer miejsca: {self.numer}, dostępność: {self.dostepne}, cena biletu: {self.cena}, udogodnienia:  {self.udogodnienia}"


# klasa zarządzająca mijescami i rezerwacjami
class Teatr:
    def __init__(self):
        self.listaMiejsc = []
        self.rezerwacje = {}
        #otworzyc plik -

    def __str__(self):
        return f"{self.listaMiejsc}"
        #return f"{self.rezerwacje}"

    def pokazListeMiejsc(self):
        for miejsce in self.listaMiejsc:
            print(miejsce)
        return True

    def pokazRezerwacje(self):
        for rezerwacja in self.rezerwacje:
            print(rezerwacja)
        return True

    def utworzMiejsce(self,parametry):
        connectToDatabase()
        zapytanie = "insert into listamiejsc values(%s,%s,%s,%s,%s,%s);"
        cursor.execute(zapytanie,parametry)
        connect.commit()


    def dostepneMiejsca(self):
        connectToDatabase()
        zapytanie = "SELECT * FROM listamiejsc where dostepne = 1;"
        cursor.execute(zapytanie)
        dane = cursor.fetchall()
        for i in dane:
            if i[5] == "zwykłe":
                print (MiejsceZwykle(i[0], i[1], i[2]))
                # print(f"m1: {m1}")
            elif i[5] == "VIP":
                print (MiejsceVIP(i[0], i[1], i[2], i[3]))
                # print(f"m1: {m1}")
            elif i[5] == "NP":
                print (MiejsceVIP(i[0], i[1], i[2], i[4]))
                # print(f"m1: {m1}")

    def zarezerwujMiejsce(self,numerMiejsca,klient):
        connectToDatabase()
        parametry = (numerMiejsca,)
        zapytanie = "SELECT * FROM listamiejsc where numer=%s and dostepne = 1;"
        cursor.execute(zapytanie,parametry)
        dane = cursor.fetchall()
        if not dane:
            print (f"Wybrane miejsce nr {numerMiejsca} jest niedostępne lub nie ma go na liście miejsc.")
            return False
        else:
            zapytanie = "update listamiejsc set dostepne = 0 where numer=%s and dostepne = 1;"
            cursor.execute(zapytanie,parametry)
            parametryRezerwacji = (None,datetime.now(),datetime.now(),"aktualna",klient,numerMiejsca,None)
            zapytanieRezerwacja = "insert into rezerwacje values (%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(zapytanieRezerwacja,parametryRezerwacji)
            connect.commit()
            dane = cursor.fetchall()
            print(f"Zarezerwowano miejsce nr {numerMiejsca}")

    def anulowanieRezerwacji(self,rezerwacja,miejsce):
        connectToDatabase()
        parametry = (miejsce,)
        zapytanie = "SELECT * FROM listamiejsc where numer=%s and dostepne = 0;"
        cursor.execute(zapytanie,parametry)
        dane = cursor.fetchall()
        if not dane:
            print (f"Wybrane miejsce nr {miejsce} nie jest zarezerwowane, nie można anulować rezerwacji.")
            return False
        else:
            zapytanie = "update listamiejsc set dostepne = 1 where numer=%s and dostepne = 0;"
            cursor.execute(zapytanie,parametry)
            parametryRezerwacji = (rezerwacja, miejsce)
            zapytanieRezerwacja = "update rezerwacje set status = 'anulowana', dataAktualizacji=CURRENT_TIMESTAMP where idRezerwacji=%s and numerMiejsca=%s"
            cursor.execute(zapytanieRezerwacja,parametryRezerwacji)
            connect.commit()
            dane = cursor.fetchall()
            #print(dane)

    def historiaRezerwacji(self,klient):
        connectToDatabase()
        parametry = (klient,)
        zapytanie = "SELECT * FROM rezerwacje where idKlienta = %s;"
        cursor.execute(zapytanie,parametry)
        dane = cursor.fetchall()
        for i in dane:
            print(f"Id rezerwacji {i[0]}, zarezerwowane miejsce nr {i[5]}, data rezerwacji {i[1]}, data aktualizacji rezerwacji {i[2]}, status rezerwacji: {i[3]}")

class Klient:
    def __init__(self, Id, Imie, Nazwisko):
        self.Id = Id
        self.Imie = Imie
        self.Nazwisko = Nazwisko

    def __str__(self):
        return f"{self.Id} {self.Imie} {self.Nazwisko}"

    def utworzKlienta(self, Id, Imie, Nazwisko):
        connectToDatabase()
        parametry = (None, Imie, Nazwisko)
        zapytanie = "insert into listaklientow values(%s,%s,%s);"
        cursor.execute(zapytanie, parametry)
        connect.commit()

def wyszukiwanieKlienta(imie,nazwisko):
    connectToDatabase()
    parametry = (imie,nazwisko)
    zapytanie = "select * FROM listaklientow where imie=%s and nazwisko=%s;"
    cursor.execute(zapytanie, parametry)
    dane = cursor.fetchall()
    if not dane:
        Klient.utworzKlienta(None, None, imie,nazwisko)
    zapytanie = "select * FROM listaklientow where imie=%s and nazwisko=%s;"
    cursor.execute(zapytanie, parametry)
    dane = cursor.fetchall()
    for i in dane:
        aktualnyKlient = i[0]
        print(aktualnyKlient)


#Tworzenie teatru
teatr = Teatr()

#Wyszukanie klienta/Utworzenie klienta
print("Id klienta")
wyszukiwanieKlienta("Anna","Kowalska")

#Pokazanie dostępnych miejsc
print("Dostępne miejsca w teatrze")
dostepneMiejsca = teatr.dostepneMiejsca()

#Rezerwacja miejsca
# teatr.zarezerwujMiejsce(12,101)

#Historia rezerwacji
teatr.historiaRezerwacji(101)

#Anulowanie rezerwacji
teatr.anulowanieRezerwacji(64,12)

#Historia rezerwacji
teatr.historiaRezerwacji(101)
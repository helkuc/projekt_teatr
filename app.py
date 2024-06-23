import mysql
import mysql.connector
from datetime import datetime
import tkinter
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox


#połączanie z bazą danych
def connectToDatabase():
    config = {"user": "root", "password": "Rozilka89!!!", "host": "localhost", "database": "teatr"}
    global connect
    connect = mysql.connector.connect(**config)
    global cursor
    cursor = connect.cursor()


# ogólna klasa miejsca
class MiejsceTeatralne:
    def __init__(self, numer, dostepne, cena):
        self.numer = numer
        self.dostepne = dostepne
        self.cena = cena


# klasa zwykłe miejsca
class MiejsceZwykle(MiejsceTeatralne):
    def __init__(self, numer, dostepne, cena):
        MiejsceTeatralne.__init__(self, numer, dostepne, cena)

    def __str__(self):
        return f"Numer miejsca: {self.numer}, dostępność: {self.dostepne}, cena biletu: {self.cena}"


# klasa VIP miejsca
class MiejsceVIP(MiejsceTeatralne):
    def __init__(self, numer, dostepne, cena, dodatkowaOplata):
        MiejsceTeatralne.__init__(self, numer, dostepne, cena)
        self.dodatkowaOplata = dodatkowaOplata

    def __str__(self):
        return f"Numer miejsca: {self.numer}, dostępność: {self.dostepne}, cena biletu: {self.cena}, dodatkowa opłata  {self.dodatkowaOplata}"


# klasa miejsca dla niepełnosprawnych
class MiejsceDlaNiepelnosprawnych(MiejsceTeatralne):
    def __init__(self, numer, dostepne, cena, udogodnienia):
        MiejsceTeatralne.__init__(self, numer, dostepne, cena)
        self.udogodnienia = udogodnienia

    def __str__(self):
        return f"Numer miejsca: {self.numer}, dostępność: {self.dostepne}, cena biletu: {self.cena}, udogodnienia:  {self.udogodnienia}"


# klasa zarządzająca mijescami i rezerwacjami
class Teatr:
    def __init__(self):
        self.listaMiejsc = []
        self.rezerwacje = []

    def utworzMiejsce(self, parametry):
        connectToDatabase()
        zapytanie = "insert into listamiejsc values(%s,%s,%s,%s,%s,%s);"
        cursor.execute(zapytanie, parametry)
        connect.commit()

    def dostepneMiejsca(self):
        connectToDatabase()
        zapytanie = "SELECT * FROM listamiejsc where dostepne = 1;"
        cursor.execute(zapytanie)
        dane = cursor.fetchall()
        self.listaMiejsc = []
        for row in dane:
            if row[5] == "zwykłe":
                self.listaMiejsc.append(MiejsceZwykle(row[0], row[1], row[2]))
            elif row[5] == "VIP":
                self.listaMiejsc.append(MiejsceVIP(row[0], row[1], row[2], row[3]))
            elif row[5] == "NP":
                self.listaMiejsc.append(MiejsceVIP(row[0], row[1], row[2], row[4]))
        return self.listaMiejsc

    def zarezerwujMiejsce(self, numerMiejsca, klient):
        connectToDatabase()
        parametry = (numerMiejsca,)
        zapytanie = "SELECT * FROM listamiejsc where numer=%s and dostepne = 1;"
        cursor.execute(zapytanie, parametry)
        dane = cursor.fetchall()
        if not dane:
            tkinter.messagebox.showinfo(title="Informacja o rezerwacji", message=f"Wybrane miejsce nr {numerMiejsca} jest niedostępne lub nie ma go na liście miejsc.")
            return False
        else:
            zapytanie = "update listamiejsc set dostepne = 0 where numer=%s and dostepne = 1;"
            cursor.execute(zapytanie, parametry)
            parametryRezerwacji = (None, datetime.now(), datetime.now(), "aktualna", klient, numerMiejsca, None)
            zapytanieRezerwacja = "insert into rezerwacje values (%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(zapytanieRezerwacja, parametryRezerwacji)
            connect.commit()
            tkinter.messagebox.showinfo(title="Informacja o rezerwacji", message=f"Zarezerwowano miejsce nr {numerMiejsca}")
            return True

    def anulowanieRezerwacji(self, miejsce):
        connectToDatabase()
        parametry = (miejsce,)
        zapytanie = "SELECT * FROM listamiejsc where numer=%s and dostepne = 0;"
        cursor.execute(zapytanie, parametry)
        dane = cursor.fetchall()
        if not dane:
            tkinter.messagebox.showinfo(title="Informacja o anulowaniu rezerwacji",
                                        message=f"Wybrane miejsce nr {miejsce} nie jest zarezerwowane, nie można anulować rezerwacji.")
            return False
        else:
            zapytanie = "update listamiejsc set dostepne = 1 where numer=%s and dostepne = 0;"
            cursor.execute(zapytanie, parametry)
            parametryRezerwacji = (miejsce,)
            zapytanieRezerwacja = "update rezerwacje set status = 'anulowana', dataAktualizacji=CURRENT_TIMESTAMP where numerMiejsca=%s"
            cursor.execute(zapytanieRezerwacja, parametryRezerwacji)
            connect.commit()
            tkinter.messagebox.showinfo(title="Informacja o anulowaniu rezerwacji",
                                        message=f"Anulowano rezerwację - miejsce nr {miejsce}.")
            return True


    def historiaRezerwacji(self, klient):
        connectToDatabase()
        parametry = (klient,)
        zapytanie = "SELECT * FROM rezerwacje where idKlienta = %s;"
        cursor.execute(zapytanie, parametry)
        dane = cursor.fetchall()
        self.rezerwacje = []
        for row in dane:
            self.rezerwacje.append(f"Id rezerwacji {row[0]}, zarezerwowane miejsce nr {row[5]}, data rezerwacji {row[1]}, data aktualizacji rezerwacji {row[2]}, status rezerwacji: {row[3]}")
        return self.rezerwacje

class Klient:
    def __init__(self, Id, Imie, Nazwisko):
        self.Id = Id
        self.Imie = Imie
        self.Nazwisko = Nazwisko

    def __str__(self):
        return f"Id klienta: {self.Id}, Imię: {self.Imie}, Nazwisko: {self.Nazwisko}"

    @staticmethod
    def utworzKlienta(Id, Imie, Nazwisko):
        connectToDatabase()
        parametry = (Id, Imie, Nazwisko)
        zapytanie = "insert into listaklientow values(%s,%s,%s);"
        cursor.execute(zapytanie, parametry)
        connect.commit()

    @staticmethod
    def obslugaKlienta(imie, nazwisko):
        connectToDatabase()
        parametry = (imie, nazwisko)
        zapytanie = "select * FROM listaklientow where imie=%s and nazwisko=%s;"
        cursor.execute(zapytanie, parametry)
        dane = cursor.fetchall()
        if not dane:
            Klient.utworzKlienta(None, imie, nazwisko)
        zapytanie = "select * FROM listaklientow where imie=%s and nazwisko=%s;"
        cursor.execute(zapytanie, parametry)
        dane = cursor.fetchall()
        id, imie, nazwisko = dane[0]
        global aktualnyKlient
        aktualnyKlient = Klient(id, imie, nazwisko)
        return aktualnyKlient


#Tworzenie teatru
teatr = Teatr()

###Porgram desktopowy
#tworzenie głownego okna programu
root = tkinter.Tk()
root.title("Rezerwacja miejsc w teatrze")
root.geometry("500x500")
#dodanie scroll
text = ScrolledText(root, state='disable')
text.pack(fill='both', expand=True)
frame = tkinter.Frame(text)
text.window_create('1.0', window=frame)

#logowanie użytkownika
labelUserName = tkinter.Label(frame, text="Podaj imię")
labelUserName.pack(pady=10)
userNameEntry = tkinter.Entry(frame)
userNameEntry.pack()
labelUserLastName = tkinter.Label(frame, text="Podaj nazwisko")
labelUserLastName.pack(pady=10)
userLastNameEntry = tkinter.Entry(frame)
userLastNameEntry.pack()


#wyświetlanie i ukrycie pól
def pola():
    #ukrycie pól po logowaniu
    labelUserName.pack_forget()
    userNameEntry.pack_forget()
    labelUserLastName.pack_forget()
    userLastNameEntry.pack_forget()
    klientButton.pack_forget()
    #wyświetlenie pól po logowaniu
    miejscaButton.pack(pady=20)
    labelMiejsce.pack()
    miejsceEntry.pack()
    rezerwujButton.pack(pady=20)
    historiaButton.pack(pady=30)
    labelMiejsceAnulowanie.pack()
    miejsceAnulowanieEntry.pack()
    anulujButton.pack(pady=20)


def pobierzDane():
    # pobieranie informacji o uzytkowniku
    givenName = str(userNameEntry.get())
    givenLastName = str(userLastNameEntry.get())
    Klient.obslugaKlienta(givenName, givenLastName)
    # wyświetlenie informacji o zalogowanym użytkowniku
    givenInfo = aktualnyKlient
    labelUserInfo = tkinter.Label(frame, text=givenInfo)
    labelUserInfo.pack()
    pola()


#przycisk logownaie
klientButton = tkinter.Button(frame, text="Logowanie", command=pobierzDane)
klientButton.pack()


#dostepne miejsa
def pokazDostepneMiesjca():
    teatr.dostepneMiejsca()
    pokazListe = teatr.listaMiejsc
    wydrukujListe = ""
    for row in pokazListe:
        wydrukujListe += (str(row) + " " + "\n")
    labelListaMiejsc = tkinter.Label(frame, text=wydrukujListe)
    labelTitleListaMiejsc = tkinter.Label(frame, text="Lista dostępnych miejsc w teatrze")
    labelTitleListaMiejsc.pack()
    labelListaMiejsc.pack()


miejscaButton = tkinter.Button(frame, text="Pokaż dostępne miejsca", command=pokazDostepneMiesjca)

#rezerwacja miejsc
labelMiejsce = tkinter.Label(frame, text="Podaj nr miejsca do rezerwacji")
miejsceEntry = tkinter.Entry(frame)


def rezerwuj():
    givenMiejsce = str(miejsceEntry.get())
    teatr.zarezerwujMiejsce(givenMiejsce, aktualnyKlient.Id)


rezerwujButton = tkinter.Button(frame, text="Zarezerwuj wskazane miejsce", command=rezerwuj)


#historia rezerwacji miejsc
def historia():
    teatr.historiaRezerwacji(aktualnyKlient.Id)
    pokazRezerwacje = teatr.rezerwacje
    wydrukujRezerwacje = ""
    for row in pokazRezerwacje:
        wydrukujRezerwacje += (str(row) + " " + "\n")
    labelTitleHistoria = tkinter.Label(frame, text="Lista rezerwacji")
    labelHistoria = tkinter.Label(frame, text=wydrukujRezerwacje)
    labelTitleHistoria.pack()
    labelHistoria.pack()


historiaButton = tkinter.Button(frame, text="Pokaż historię rezerwacji miejsc", command=historia)

#anulowanie rezerwacji
labelMiejsceAnulowanie = tkinter.Label(frame, text="Podaj nr miejsca do anulowania")
miejsceAnulowanieEntry = tkinter.Entry(frame)


def anuluj():
    givenMiejsceAnulowanie = str(miejsceAnulowanieEntry.get())
    teatr.anulowanieRezerwacji(givenMiejsceAnulowanie)


anulujButton = tkinter.Button(frame, text="Anulowanie rezerwacji", command=anuluj)

#powtarzanie kodu w pętli
frame.mainloop()

# #Wyszukanie klienta/Utworzenie klienta
# print("Id klienta")
# Klient.obslugaKlienta("Anna", "Kow")
#
# #Pokazanie dostępnych miejsc
# print("Dostępne miejsca w teatrze")
# dostepneMiejsca = teatr.dostepneMiejsca()
#
#Rezerwacja miejsca
# teatr.zarezerwujMiejsce(12, 101)
#
# #Historia rezerwacji
# teatr.historiaRezerwacji(101)
#
# #Anulowanie rezerwacji
# teatr.anulowanieRezerwacji(12)

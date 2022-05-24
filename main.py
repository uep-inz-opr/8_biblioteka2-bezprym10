class Ksiazka:

    def __init__(self, tytul: str, autor: str):
        self.tytul = tytul
        self.autor = autor


class Egzemplarz:

    def __init__(self, rok_wydania: int, ksiazka: Ksiazka):
        self.tytul = ksiazka.tytul
        self.autor = ksiazka.autor
        self.rok_wydania = rok_wydania
        self.wypozyczony = False


class Czytelnik:

    def __init__(self, nazwisko: str, limit_wypozyczen: int):
        self.nazwisko = nazwisko
        self.limit_wypozyczen = limit_wypozyczen
        self.wypozyczone_ksiazki = []

    def wypozycz(self, egzemplarz: Egzemplarz) -> bool:
        if len(self.wypozyczone_ksiazki) < self.limit_wypozyczen:
            for egz in self.wypozyczone_ksiazki:
                if egzemplarz.tytul == egz.tytul:
                    return False
            self.wypozyczone_ksiazki.append(egzemplarz)
            return True
        return False
    
    def oddaj(self, tytul: str) -> bool:
        for egz in self.wypozyczone_ksiazki:
            if egz.tytul == tytul:
                self.wypozyczone_ksiazki.remove(egz)
                return True
        return False


class Biblioteka:

    def __init__(self, limit_wypozyczen: int):
        self.limit_wypozyczen = limit_wypozyczen
        self.dostepne_egz = []
        self.wypozyczone_egz = []
        self.dostepne_ksiazki = []
        self.czytelnicy = []

    def __sprawdz_czytelinka(self, nazwisko: str) -> Czytelnik:
        for czytelnik in self.czytelnicy:
            if czytelnik.nazwisko == nazwisko:
                return czytelnik
        nowy_czytelnik = Czytelnik(nazwisko=nazwisko,
                                   limit_wypozyczen=self.limit_wypozyczen)
        self.czytelnicy.append(nowy_czytelnik)
        return nowy_czytelnik
    
    def dostepne_egzem(self, tytul: str) -> list:
        dostepne_pod_tytulem = []
        for egz in self.dostepne_egz:
            if egz.tytul == tytul:
                dostepne_pod_tytulem.append(egz) 
        return dostepne_pod_tytulem

    def wypozycz(self, nazwisko: str, tytul: str) -> bool:
        czytelnik = self.__sprawdz_czytelinka(nazwisko=nazwisko)
        if len(self.dostepne_egzem(tytul=tytul)) >= 1:
            egz = self.dostepne_egzem(tytul=tytul)[0]
            wypozyczony = czytelnik.wypozycz(egzemplarz=egz)
            if wypozyczony:
                self.dostepne_egz.remove(egz)
                self.wypozyczone_egz.append(egz)
                return True
        return False
            
    def oddaj(self, nazwisko: str, tytul: str) -> bool:
        czytelnik = self.__sprawdz_czytelinka(nazwisko=nazwisko)
        for egz in self.wypozyczone_egz:
            if egz.tytul == tytul:
                if czytelnik.oddaj(tytul=tytul):
                    self.wypozyczone_egz.remove(egz)
                    self.dostepne_egz.append(egz)
                    return True 
        return False

    def dodaj_egzemplarz_ksiazki(self, tytul: str, autor: str, rok_wydania: int) -> bool:
        wybrana_ksiazka = None
        for ksiazka in self.dostepne_ksiazki:
            if ksiazka.tytul == tytul and ksiazka.autor == autor:
                wybrana_ksiazka = ksiazka
        if wybrana_ksiazka == None:
            wybrana_ksiazka = Ksiazka(tytul=tytul, autor=autor)
            self.dostepne_ksiazki.append(wybrana_ksiazka)
        self.dostepne_egz.append(Egzemplarz(rok_wydania=rok_wydania, ksiazka=wybrana_ksiazka))
        return True


n = int(input("Podaj liczbę akcji: "))
biblio = Biblioteka(limit_wypozyczen=3)
for _ in range(n):
    krotka = eval(input("Wprowadź akcję: "))
    if krotka[0].strip() == "dodaj":
        biblio.dodaj_egzemplarz_ksiazki(tytul=krotka[1], autor=krotka[2], rok_wydania=krotka[3])
    elif krotka[0].strip() == "wypozycz":
        biblio.wypozycz(nazwisko=krotka[1], tytul=krotka[2])
    elif krotka[0].strip() == "oddaj":
        biblio.oddaj(nazwisko=krotka[1], tytul=krotka[2])

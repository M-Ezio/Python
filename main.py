import tkinter as tk
from tkinter import filedialog
import math
import datetime

class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff=''
        #freq = czestotliwość wystąpienia
        #symbol = litera alfabetu
        #left = lewy węzeł drzewa
        #right = prawy węzeł drzewa

dl=[] # lista przechowująca długości słów kodowych
kod=[] # lista przechowująca symbol oraz jego kod Huffman'a
srDlugosc=[] # lista przechowująca średnią długość kodową(pobiera wynik tylko raz)
entr=[] # lista przechowująca entropię (pobiera wynik tylko raz)

def printNodes(node, val=''):
   newVal= val+str(node.huff)#newVal = kod Huffmana dla danego węzła

   # jeżeli węzeł nie jest węzłem krawędziowym, porusza się w głąb
   if node.left:
        printNodes(node.left, newVal)
   if node.right:
        printNodes(node.right, newVal)
   #jeżeli węzeł jest węzłem krawędziowym, wyświetl kod Huffmana
   if(not node.left and not node.right and node.symbol!=" " and node.symbol !="\n"):
        print(f"{node.symbol}->{newVal}") # wypisanie znaku oraz jego kodu huffmana
        dl.append(len(newVal))#dodanie długości słowa kodowego od listy "dl"
        kod.append(f"{node.symbol}->{newVal} ")#dodanie symbolu oraz jego kodu jako tekst do listy "kod"
   elif (not node.left and not node.right and node.symbol==" "): #jeżeli symbol to " " zapisany zostaje jako space
       print(f"space->{newVal}")
       dl.append(len(newVal))
       kod.append(f"space->{newVal} ")
   elif (not node.left and not node.right and node.symbol=="\n"): #jeżeli symbol to "\n"(znak nowej linii) symbol zapisany zostaje jako newline
       print(f"newline->{newVal}")
       dl.append(len(newVal))
       kod.append(f"newline->{newVal} ")



def srDl(alfabet, dlugosci, wystapienia): #funkcja w której obliczana jest średnia długość słowa kodowego
    #funkcja przyjmuje listę w której znajduje się nasz alfabet, listę w której znajdują się długości słów kodowych
    #oraz listę w której znajdują się częstotliwości występowania elementów alfabetu

    tmp=0 #tymczasowa zmienna przechowująca wartość
    suma=sum(wystapienia) #suma wszystkich prawdopodobieństw
    lengths=dlugosci #wczytanie listy w której znajdują się długości słów kodowych
    for i in range(len(alfabet)): #pętla przechodząca od początku do końca alfabetu
        tmp=tmp+int(lengths[i])*int(wystapienia[i])/int(suma) #suma wyniku zwiększająca się z każdą iteracją pentli
    tmp=round(tmp,4)# zaokrąglenie wyniku do 4 miejsc po przecinku
    print("Srednia długość słowa kodowego E(K) = " + str(tmp)) # wypisanie w konsoli wyniku
    srDlugosc.append(tmp) # dodanie wyniku do listy "srDlugosc"

def entropia(alfabet, wystapenia): #funkcja w której obliczana jest entropia
    wynik=0 # zmienna w której zapisany jest nasz wynik
    suma=sum(wystapenia) #suma wszystkich prawdopodobieństw
    for i in range(len(alfabet)):  #pętla przechodząca od początku do końca alfabetu
        wynik=wynik-(wystapenia[i]/suma*math.log2(wystapenia[i]/suma)) #suma wszystkich wyników
    wynik=round(wynik,4) # zaokrąglenie wyniku do 4 miejsc po przecinku
    entr.append(wynik) # dodanie wyniku do listy "entr"
    print("Entropia H(pi,...,pn) = " + str(wynik)) # wypisanie wyniku w konsoli

def unikalne(wiadomosc): # funkcja wyciąga wszystkie unikalne znaki bez powtórzeń z wiadomości
    lista=[] # lista przechowująca wszystkie unikalne znaki
    for i in wiadomosc: # petla poruszająca się od początku do końca naszej wiadomości, idąc element po elemencie
        if i not in lista: # jeżeli element nie znajduje się w liscie zostaje do niej dodany
            lista.append(i)
    return lista # zwracanie listy

def zliczWystapienia(wiadomosc, unik): #funkcja zliczająca wystąpienia unikalnych znaków w wiadomości
    list=sorted(wiadomosc) # sortowanie wiadomości i zapisanie w zmiennej list
    wystapienia=[] # lista przechowująca wystąpienia
    for i in range(len(unik)): # pętla  przechodząca od początku do końca listy unikalnych znaków
        tmp=list.count(unik[i]) # zliczanie powtórzeń
        wystapienia.append(tmp) # dodanie wystąpień do listy
    return wystapienia # zwrócenie listy wystąpień

def wyliczanieKodu(unik, wystapienia): # funkcja wyliczająca kod Huffmana
    symbole=unik # wczytanie listy unikalnych znaków
    wyst=wystapienia # wczytanie listy wystąpień
    wezly=[] # lista przechowująca węzły

    for i in range(len(symbole)): # pętla  przechodząca od początku do końca listy unikalnych znaków
        wezly.append(node(wyst[i],symbole[i])) # dodanie do listy węzłów

    while len(wezly) > 1: # pętla warunkowa, wykonuje się ona dopóku liczba węzłów nie będzie równa 1
        wezly = sorted(wezly, key=lambda x: x.freq) # sortowanie węzłów

        left = wezly[0] # węzeł będący po lewej
        right = wezly[1] # węzeł będący po prawej

        left.huff = 0 # przypisanie 0 do lewego węzłą
        right.huff = 1 # przypisanie 1 do prawego wezłą

        newWezel = node(left.freq+right.freq, left.symbol+right.symbol, left, right) # utworzenie nowego węzła poprzez dodanie prawego węzła oraz lewego węzła do siebie

        wezly.remove(left) #usunięcie lewego węzłą
        wezly.remove(right) # usunięcie prawego węzłą
        wezly.append(newWezel) # dodanie nowego węzła składającego się z prawego oraz lewego węzła

    printNodes(wezly[0]) # wypisanie wyników w konsoli


def wczytajWiadomosc(wiadomosc): # funkcja wczytująca wiadomość
    message=sorted(wiadomosc) # sortowanie wiadomości
    unik=unikalne(message) # utworzenie listy unikalnych znaków
    wyst=zliczWystapienia(message,unik) # utworzenie listy zawierającej wystąpenia unikalnych znaków
    wyliczanieKodu(unik,wyst) # wyliczenie oraz wypisanie kodu Huffmana
    srDl(unik,dl,wyst) # wyliczenie oraz wypisanie średniej długości słowa kodowego
    entropia(unik,wyst) # wyliczenie oraz wypisanie entropii


print("Opcje")
print("1 - Wczytaj z pliku")
print("2 - Wpisz wiadomość z klawiatury")
x=input() # funkcja pobierająca wartość z klawiatury
x=int(x) # zamiana typu na int
while(x>2): # jeżeli x większe od 2 pętla będzie się powtarzać
    print("Nie ma takiej opcji")
    print("Wybierz opcję ponownie")
    print("1 - Wczytaj z pliku")
    print("2 - Wpisz wiadomość z klawiatury")
    x=input()
    x=int(x)

if x==1:
    root = tk.Tk()
    print("Wybierz plik zawierający wiadomość")
    file_path = filedialog.askopenfilename() # zapisanie ścieżki do pliku
    plik=open(file_path) # otworzenie pliku z podanej ścieżki
    root.withdraw() # zamknięcie okna
    message=plik.read() # zapisanie wiadomości do zmiennej
    plik.close() # zamknięcie pliku
    wczytajWiadomosc(message) # wczytanie wiadomości
    print("Czy chcesz zapisać do pliku txt? (tak/nie)")
    opcja=input() # funkcja pobierająca wartość z klawiatury
    if opcja=="tak":
        data = datetime.datetime.now() # funkcja przechowywująca obecny czas oraz datę
        data = data.strftime("%d/%m/%Y %H:%M:%S") # format w jakim zapisana jest data
        outputfile = open("output.txt", 'a') # wczytanie i utworzenie(jeżeli nie istnieje) pliku w którym zapisywane są dane, z opcją dopisu danych
        outputfile.write("========================= |" + str(data) + "| =========================\n")
        for i in range(len(kod)):
            outputfile.write(kod[i] + "\n") # zapisanie kodu linia po linii do pliku
        outputfile.write("\nSrednia długość słowa kodowego E(K) = " + str(srDlugosc[0])) # zapisanie średniej długości słowa kodowego do pliku
        outputfile.write("\nEntropia H(pi,...,pn) = " + str(entr[0])) # zapisanie entropii do pliku
        outputfile.write("\n=========================================================================\n")
        print("Plik jest w tym samym katalogu co projekt")
        print("Program zakończył działanie")
        outputfile.close() # zamknięcie pliku
    if opcja=="nie":
        print("Program zakończył działanie")

if x==2:
    print("Wpisz wiadomość")
    message=input() # wczytanie wiadomości z klawiatury
    print("Wpisana wiadomość = " + str(message))
    wczytajWiadomosc(message)
    print("Czy chcesz zapisać do pliku txt? (tak/nie)")
    opcja = input()
    if opcja == "tak":
        data = datetime.datetime.now()
        data = data.strftime("%d/%m/%Y %H:%M:%S")
        outputfile = open("output.txt", 'a')
        outputfile.write("========================= |" + str(data) + "| =========================\n")
        for i in range(len(kod)):
            outputfile.write(kod[i] + "\n")
        outputfile.write("\nSrednia długość słowa kodowego E(K) = " + str(srDlugosc[0]))
        outputfile.write("\nEntropia H(pi,...,pn) = " + str(entr[0]))
        outputfile.write("\n=========================================================================\n")
        print("Plik jest w tym samym katalogu co projekt")
        print("Program zakończył działanie")
        outputfile.close()
    if opcja=="nie":
        print("Program zakończył działanie")

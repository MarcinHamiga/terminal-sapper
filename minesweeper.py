from random import randint
from copy import deepcopy
from colorama import Fore, Style, Back
from time import sleep
import platform
import os

def clear():    # Czyści ekran, nic takiego
    if platform.system().lower() == "linux":    # Sprawdza na jakim systemie operacyjnym jesteśmy. Jeżeli to linux, to używa systemowej komendy clear
        os.system("clear")
    if platform.system().lower() == "windows":  # Jeżeli to winda, to używa upośledzonego cls
        os.system("cls")

def get_number(a: int, b: int, text: str) -> int:
    while True: 
        try:    # Będziemy sobie testować, czy coś się nie wysypie.
            number = int(input(text))   # Se bierzemy input od usera i go rzutujemy na inta. Tak o fajnie.
            if a <= number <= b:
                return number
            else:
                print("Enter a valid number!")
                sleep(1)
        # Sprawdzamy, czy input usera może w ogóle zostać zrzutowany na inta. Jeżeli ni, to powód jest nieważny,
        # lecimy tutaj i karcimy usera, ze ma wpisac inta
        except ValueError:
            print("Enter an integer!")
            sleep(1)
        # To jest ważne, bo jak bez tego zachce nam się robić pusty except, to nawet ctrl + c nie pozwoli nam wyjśc (ctrl + c wywołuje KeyboardInterrupt exception)
        except KeyboardInterrupt:
            clear()
            exit()
        # Jak wywali się coś, czego nie przewidujemy, to odpala się to, ez.
        except:
            print("Something went wrong. Please try again.")
            sleep(2)
        

def lay_mines(a: int, b: int, mines_num: int) -> set:
    mines = set()   # Tworzymy nowy set (Nie, zrobienie tego klamerkami NIE działa. Tworzycie wtedy słownik a nie set.)
    for x in range(0, mines_num + 1):
        mines.add((randint(0, a-1), randint(0, b-1)))   # Set ma metodę add zamiast append. Do zapamiętania.
    return mines

def number_of_neighbouring_mines(x: int, y: int, board: list) -> int:
    if board[x][y] == "B":
        return -1
    neigh_mines = 0
    for n in range(x-1, x+2):   # Pętla sprawdzająca wiersze
        for m in range(y-1, y+2):   # Pętla sprawdzająca kolumny
            if 0 <= n < len(board) and 0 <= m < len(board[n]):
                if board[n][m] == "B":
                    neigh_mines += 1
            else:
                continue   
    return neigh_mines 

def create_board(m: int, n: int, mines: set):
    # Generowanie pustej listy board
    board = []
    for row in range(m):    # Pętla wierszy
        board.append([])    # Dodawanie list do listy, aby utworzyć listę dwuwymiarową
        for col in range(n):    # Pętla kolumn
            board[row].append(0)    # Wprowadzanie wartości 0 do każdej komórki w liście
    
    mask = deepcopy(board)  # Stworzenie maski poprzez głęboką kopię listy board
    
    for mine in mines:  # Pętla służąca rozlokowaniu min
        x, y = mine # Rozpakowanie krotki mine
        board[x][y] = "B"   # Rozlokowanie min na planszy

    # Tutaj dzieje się kongo
    for i, row in enumerate(board): 
        for j, col in enumerate(row):
            number = number_of_neighbouring_mines(i, j, board) # Szukamy ile bomb ma dookoła siebie każde pole
            if number == -1:
                continue    # Jak pole jest bombą to nic nie robimy, zostawiamy tam ładnie 'B'
            else:
                row[j] = number # Jak pole nie jest bomba, to ładujemy tam liczbę bomb dookoła
    return board, mask

def reveal_fields(m: int, n: int, x: int, y: int, board: list, mask: list):
    if board[x][y] == "B": # Jak bum bum no to przegrywasz byq
        mask[x][y] = 1
        print("You lost!")
        return -1
    if mask[x][y] == 1: # Jak pole już było odkryte, to zakańczamy wykonanie funkcji, aby uniknąć nieskończonej rekurencji
        return 0
    
    if board[x][y] == 0:    # Jak pole nie ma dookoła min, no to generalnie bajlando. Lecimy na pole po lewej, po prawej, poniżej i powyżej.
        mask[x][y] = 1  # Oznaczamy pole jako odkryte
        if x - 1 > -1:
            reveal_fields(m, n, x - 1, y, board, mask)
        if x + 1 <= m-1:
            reveal_fields(m, n, x + 1, y, board, mask)
        if y - 1 > -1:
            reveal_fields(m, n, x, y - 1, board, mask)
        if y + 1 <= n-1:
            reveal_fields(m, n, x, y + 1, board, mask)
    if 0 < board[x][y] < 9: # Jak pole ma dookoła miny, to oznaczamy je jako odkryte ale nie lecimy już na następne pola
        mask[x][y] = 1 

def print_board(m: int, n: int, board: list, mask: list):
    rows = 1
    cols = 1
    print(f"{'':<3}", end="")   # Dużo printów, a generalnie <3 pozwala nam na sztywno ustawić, że wyrażenie w klamerce ma zostać zapisane na trzech pozycjach w terminalu.
    for x in range(m):
        print(f"{Fore.RED}{f'{cols}':<3}{Style.RESET_ALL}", end="")    # Inna liczba, np <4 ustawi na sztywno, że ma zająć 4 miejsca.
        cols += 1
    print()
    for row_b, row_m in zip(board, mask):   # Zipujemy sobie dwie listy, zeby móc iterować po obu na raz.
        print(f"{Fore.RED}{f'{rows}':<3}{Style.RESET_ALL}", end="")
        rows += 1
        for col_b, col_m in zip(row_b, row_m):
            if col_m == 0:
                print(f"{Fore.BLUE}{'?':<3}{Style.RESET_ALL}", end="")
            else:
                if col_b == 0:
                    print(f"{Back.GREEN}{' ':<3}{Style.RESET_ALL}", end="")
                else:
                    print(f"{Fore.CYAN}{col_b:<3}{Style.RESET_ALL}", end="")
        print()
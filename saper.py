from minesweeper import *
import platform
import os

def saper():
    is_running = True
    m = get_number(8, 30, f"Enter a number(8-30):")
    n = get_number(8, 24, f"Enter a number(8-24):")
    
    max_mines = (m-1) * (n-1)
    num_mines = get_number(10, max_mines, f"Enter a number of mines(10-{max_mines})")

    mines = lay_mines(m, n, num_mines)

    board, mask = create_board(m, n, mines)
    print_board(m, n, board, mask)
    while is_running:
        x = get_number(0, m, f"Enter a row (1-{m}): ") - 1
        y = get_number(0, n, f"Enter a column (1-{n}): ") - 1

        clear()

        lose = reveal_fields(m, n, x, y, board, mask)
        if lose == -1:
            is_running = False
        print_board(m, n, board, mask)
    input("---press Enter to exit---")
saper()
import curses
from minesweeper import *

class Minesweeper:
    
    def __init__(self, root):
        self.ROOT = root
        
        self.MAX_ROWS = 30
        self.MIN_ROWS = 8
        self.MAX_COLS = 24
        self.MIN_COLS = 8
        
        self.rows = 8
        self.cols = 8
     
        self.num_mines = 10
        
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        
        self.colors = {
            "cursor" : curses.color_pair(1),
            0 : curses.color_pair(2),
            1 : curses.color_pair(3),
            2 : curses.color_pair(3),
            3 : curses.color_pair(3),
            4 : curses.color_pair(3),
            5 : curses.color_pair(3),
            6 : curses.color_pair(3),
            7 : curses.color_pair(3),
            8 : curses.color_pair(3)
            
        }
        
        
        
        self._spacebar = ord(" ")
        self._e_key = ord("e")
        self._a_key = ord("a")
        
    def start_screen(self):
        self.ROOT.nodelay(True)
        option = 1
        start_scr = True
        while start_scr:
            max_mines = (self.rows-1) * (self.cols-1)
            if self.num_mines > max_mines:
                self.num_mines = max_mines 
            self.ROOT.refresh()
            if option == 1:
                self.ROOT.addstr(0, 0, f"Number of rows of the board (max: {self.MAX_ROWS}): {self.rows} <--")
            else:
                self.ROOT.addstr(0, 0, f"Number of rows of the board (max: {self.MAX_ROWS}): {self.rows}")
            if option == 2:
                self.ROOT.addstr(1, 0, f"Number of columns of the board (max: {self.MAX_COLS}): {self.cols} <--")
            else:
                self.ROOT.addstr(1, 0, f"Number of columns of the board (max: {self.MAX_COLS}): {self.cols}")
            if option == 3:
                self.ROOT.addstr(2, 0, f"Number of mines (max: {(self.rows-1) * (self.cols-1)}): {self.num_mines} <--")
            else:
                self.ROOT.addstr(2, 0, f"Number of mines (max: {(self.rows-1) * (self.cols-1)}): {self.num_mines}")
            self.ROOT.addstr(4, 0, "Press 'a' to accept these settings.")
            self.ROOT.addstr(5, 0, "Use the arrow keys to navigate.")
            self.ROOT.addstr(6, 0, "When in-game, use the spacebar to reveal the currently highlighted field.")
            usr_input = self.ROOT.getch()
            match usr_input:
                
                case curses.KEY_RIGHT:  # To, co dzieje się kiedy wciśniemy prawą strzałkę
                    if self.rows < self.MAX_ROWS and option == 1:
                        self.rows += 1
                    elif self.cols < self.MAX_COLS and option == 2:
                        self.cols += 1
                    elif self.num_mines < max_mines and option == 3:
                        self.num_mines += 1
                    self.ROOT.clear()
                    
                case curses.KEY_LEFT:   # To, co dzieje się kiedy wciśniemy lewą strzałkę
                    if self.rows > self.MIN_ROWS and option == 1:
                        self.rows -= 1
                    elif self.cols > self.MIN_COLS and option == 2:
                        self.cols -= 1
                    elif self.num_mines > 10 and option == 3:
                        self.num_mines -= 1
                    self.ROOT.clear()
                    
                case curses.KEY_UP: # To, co dzieje się kiedy wciśniemy strzałkę do góry
                    if option > 1:
                        option -= 1
                    self.ROOT.clear()
                    
                case curses.KEY_DOWN:   # To, co dzieje się kiedy wciśniemy strzałkę w dół
                    if option < 3:
                        option += 1
                    self.ROOT.clear()
                    
                case self._a_key:
                    start_scr = False
                    self.ROOT.clear()
                    
                case _:
                    continue
                  
    def print_board(self, board, mask, cursor_row, cursor_col):
        for i, rows in enumerate(board):
                spacing = 0
                for j, cols in enumerate(rows):
                    if (i, j) == (cursor_row, cursor_col):
                        if mask[i][j] == 1:
                            self.ROOT.addstr(i, spacing, f" {cols} ", self.colors["cursor"])
                        else:
                            self.ROOT.addstr(i, spacing, f" ? ", self.colors["cursor"])
                    else:
                        if mask[i][j] == 1:
                            self.ROOT.addstr(i, spacing, f" {cols} ", self.colors[cols])
                        else:
                            self.ROOT.addstr(i, spacing, f" ? ")
                    spacing += 3
                    
    def game_screen(self):
        self.ROOT.nodelay(True)
        mines, final_num_mines = lay_mines(self.rows, self.cols, self.num_mines)

        board, mask = create_board(self.rows, self.cols, mines)
        game_on = True
        cursor_row = 0
        cursor_col = 0

        while game_on:
            self.print_board(board, mask, cursor_row, cursor_col)
            usr_input = self.ROOT.getch()
            match usr_input:
                case curses.KEY_UP:
                    if cursor_row > 0:
                        cursor_row -= 1
                case curses.KEY_DOWN:
                    if cursor_row < self.rows - 1:
                        cursor_row += 1
                case curses.KEY_LEFT:
                    if cursor_col > 0:
                        cursor_col -= 1
                case curses.KEY_RIGHT:
                    if cursor_col < self.cols - 1:
                        cursor_col += 1
                case self._spacebar:
                    lose = reveal_fields(self.rows, self.cols, cursor_row, cursor_col, board, mask)
                    if lose == -1:
                        self.print_board(board, mask, cursor_row, cursor_col)
                        self.ROOT.refresh()
                        self.ROOT.addstr(self.rows + 2, 0, "You lost!")
                        self.ROOT.refresh()
                        curses.napms(2000)
                        game_on = False
                case self._e_key:
                    game_on = False
            count = 0
            for row in mask:
                for col in row:
                    if col == 1:
                        count += 1
                    if self.rows * self.cols - final_num_mines == count:
                        self.ROOT.addstr(self.rows + 2, 0, "You win!")
                        game_on = False
            self.ROOT.refresh()
            
scr = curses.initscr()
def main(scr):
    game = Minesweeper(scr)
    game.start_screen()
    game.game_screen()
    
    
if __name__ == "__main__":
    curses.wrapper(main)
    
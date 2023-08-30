import random
import tkinter as tk
from MyButton import MyButton
from tkinter.messagebox import showinfo
from Menu import Menu
from Field import Field

colors = ['#BBB', "blue", "green", "yellow", "brown", "violet", "blue", "orange"]


class MineSweeper:
    ROW = 10
    COL = 7
    COUNT_MINES = 5
    window = tk.Tk()
    positions = []
    is_game_over = False

    def __init__(self):
        self.window.title("Minesweeper")
        self.menu = Menu(self.window, self)
        self.field = Field(self)

    def right_click(self, event: tk.Event):

        if self.is_game_over:
            return

        current_button: MyButton = event.widget

        if current_button["state"] == "normal":
            current_button.config(state="disabled", text="🚩", disabledforeground="#CC0000")
        elif current_button["text"] == "🚩":
            current_button.config(text="", state="normal")

    def create_widgets(self):

        self.menu.init_sett_bar()

        for row in range(1, self.ROW + 1):
            for col in range(1, self.COL + 1):
                button = self.field.field[row][col]

                button.grid(row=row, column=col, stick="NWES")

        for i in range(1, self.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, self.COL + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def reload(self):
        for child in self.window.winfo_children():
            child.destroy()

        self.__init__()
        self.init_mines_positions()
        self.insert_mines()
        self.count_mines_in_ceils()
        self.create_widgets()
        self.is_game_over = False

    def start_game(self):
        self.init_mines_positions()
        self.insert_mines()
        self.count_mines_in_ceils()
        # self.open_all_buttons()
        self.create_widgets()

        self.window.mainloop()

    def init_mines_positions(self):
        positions = []
        while len(positions) < self.COUNT_MINES:
            pos = random.randint(1, self.ROW * self.COL)

            if pos in positions:
                continue
            else:
                positions.append(pos)

        self.positions = positions

    def insert_mines(self):
        count = 1
        for row_index in range(1, self.ROW + 1):
            for col_index in range(1, self.COL + 1):
                button: MyButton = self.field.field[row_index][col_index]
                button.number = count
                count += 1
                if button.number in self.positions:
                    button.is_mine = True
                    print(button)

    def count_mines_in_ceils(self):
        for row_index in range(1, self.ROW + 1):
            for col_index in range(1, self.COL + 1):

                button: MyButton = self.field.field[row_index][col_index]
                count_bombs = 0

                if not button.is_mine:

                    for row_idx in [-1, 0, 1]:
                        for col_idx in [-1, 0, 1]:
                            neighbour: MyButton = self.field.field[row_index + row_idx][col_index + col_idx]
                            if neighbour.is_mine:
                                count_bombs += 1

                button.count_bomb = count_bombs

    def click(self, clicked_button: MyButton):

        if self.is_game_over:
            return

        if clicked_button.is_mine:

            clicked_button.config(text="*")
            clicked_button.is_open = True
            self.is_game_over = True

            for row in range(1, self.ROW + 1):
                for col in range(1, self.COL + 1):
                    button: MyButton = self.field.field[row][col]

                    if button.is_mine:
                        button.config(text="*", background="black", fg="white")

            showinfo("Проигрыш", "Вы проиграли")

        else:
            if clicked_button.count_bomb:

                clicked_button.config(text=clicked_button.count_bomb, fg=colors[clicked_button.count_bomb],
                                      disabledforeground=colors[clicked_button.count_bomb])
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)

        clicked_button.config(relief=tk.SUNKEN, state="disabled")
        self.check_win()

    def check_win(self):

        count_btn = self.COL * self.ROW

        disabled = 0

        for row_index in range(self.ROW + 2):
            for col_index in range(self.COL + 2):
                button: MyButton = self.field.field[row_index][col_index]

                if button['state'] == "disabled":
                    disabled += 1

        if (count_btn - self.COUNT_MINES) == disabled and not self.is_game_over:
            showinfo("Победа", "Поздравляю, вы победили")
            self.is_game_over = True

    def open_all_buttons(self):
        for row_index in range(self.ROW + 2):
            for col_index in range(self.COL + 2):
                button: MyButton = self.field.field[row_index][col_index]

                if button.is_mine:
                    button.config(text="*", background="red")
                else:
                    button.config(text=button.count_bomb, foreground=colors[button.count_bomb])

    def breadth_first_search(self, button: MyButton):
        queue: list[MyButton] = [button]

        while queue:
            current_button = queue.pop()
            color = colors[current_button.count_bomb]

            if current_button.count_bomb:
                current_button.config(text=current_button.count_bomb, disabledforeground=color)
            else:
                current_button.config(text="", disabledforeground=color)

            current_button.is_open = True

            current_button.config(state="disabled", relief=tk.SUNKEN)

            if current_button.count_bomb == 0:
                #
                x, y = current_button.x, current_button.y

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue

                        next_button: MyButton = self.field.field[x + dx][y + dy]

                        if (
                                not next_button.is_open
                        ) and (
                                1 <= next_button.x <= self.ROW
                        ) and (
                                1 <= next_button.y <= self.COL
                        ) and (
                                next_button not in queue
                        ):
                            queue.append(next_button)


game = MineSweeper()
game.start_game()

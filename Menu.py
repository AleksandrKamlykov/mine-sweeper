import tkinter as tk
from tkinter.messagebox import  showerror


class Menu:

    def __init__(self, window: tk.Tk, target):
        self.window: tk.Tk = window
        self.target = target

    def create_setting(self):
        settings = tk.Toplevel(self.window)
        settings.title("Настройки")

        tk.Label(settings, text="Колличество строк").grid(row=0, column=0)
        tk.Label(settings, text="Колличество столбцов").grid(row=1, column=0)
        tk.Label(settings, text="Колличество мин").grid(row=2, column=0)

        row_entry = tk.Entry(settings)
        columns_entry = tk.Entry(settings)
        mines_entry = tk.Entry(settings)

        row_entry.grid(row=0, column=1, padx=20, pady=20)
        columns_entry.grid(row=1, column=1, padx=20, pady=20)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        row_entry.insert(0, self.target.ROW)
        columns_entry.insert(0, self.target.COL)
        mines_entry.insert(0, self.target.COUNT_MINES)

        tk.Button(settings, text="Применить",
                  command=lambda: self.change_settings(row_entry, columns_entry, mines_entry)).grid(row=3,
                                                                                                    column=1)

    def change_settings(self, row: tk.Entry, col: tk.Entry, mines: tk.Entry):
        try:
            self.target.ROW = int(row.get())
            self.target.COL = int(col.get())
            self.target.COUNT_MINES = int(mines.get())
            self.target.reload()
        except ValueError:
            showerror("Ошибка", "Значение может быть только числом")

        return

    def init_sett_bar(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Играть", command=self.target.reload)
        settings_menu.add_command(label="Настройки", command=self.create_setting)
        settings_menu.add_command(label="Выход", command=self.window.destroy)

        menubar.add_cascade(label="Опции", menu=settings_menu)

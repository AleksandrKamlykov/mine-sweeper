import tkinter as tk


class MyButton(tk.Button):

    def __init__(self, master, x, y, number, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False
        self.number = number
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f"MyButton {self.number}, {self.is_mine}"

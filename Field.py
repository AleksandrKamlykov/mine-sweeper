from MyButton import MyButton


class Field:
    field = []

    def __init__(self, target):
        self.target = target
        self.create_field()

    def create_field(self):
        self.field = []
        for row_item in range(self.target.ROW + 2):

            row_buttons = []

            for col_item in range(self.target.COL + 2):
                button = MyButton(self.target.window, x=row_item, y=col_item, number=0, width=3,
                                  font="Calibri 15 bold")
                button.config(command=lambda btn=button: self.target.click(btn))
                button.bind("<Button-3>", self.target.right_click)
                row_buttons.append(button)

            self.field.append(row_buttons)

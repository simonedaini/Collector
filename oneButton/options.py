from lib2to3.pgen2.token import OP
from tkinter import *

class Options():
    def __init__(self, parent, option_list):
        self.parent = parent
        self.options = option_list

        self.om_variable = StringVar(self.parent)
        self.om_variable.set(self.options[0])
        self.om_variable.trace('w', self.option_select)

        self.om = OptionMenu(self.parent, self.om_variable, *self.options)
        self.om.grid(column=0, row=0)

        self.label = Label(self.parent, text='Enter new option')
        self.entry = Entry(self.parent)
        self.button = Button(self.parent, text='Add option to list', command=self.add_option)

        self.label.grid(column=1, row=0)
        self.entry.grid(column=1, row=1)
        self.button.grid(column=1, row=2)

        self.update_button = Button(self.parent, text='Update option menu', command=self.update_option_menu)
        self.update_button.grid(column=0, row=2)

    def update_option_menu(self):
        menu = self.om["menu"]
        menu.delete(0, "end")
        for string in self.options:
            menu.add_command(label=string, 
                             command=lambda value=string: self.om_variable.set(value))

    def add_option(self):
         self.options.append(self.entry.get())
         self.entry.delete(0, 'end')
         print(self.options)

    def option_select(self, *args):
        print(self.om_variable.get())


root = Tk()
Options(root, ["EAV", "FS"])
root.mainloop()

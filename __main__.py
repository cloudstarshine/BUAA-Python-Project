from tkinter import *
import login


class BaseDesk:
    def __init__(self, master):
        self.root = master
        self.root.geometry('1000x750+200+100')
        login.Login(self.root)
        self.root.mainloop()


if __name__ == '__main__':
    root = Tk()
    root.resizable(width=None, height=None)
    BaseDesk(root)

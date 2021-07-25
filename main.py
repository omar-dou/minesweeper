import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from matplotlib.pyplot import imshow
import numpy
import random
import os

class MyButton(ttk.Button):

    def __init__(self, tk, hasbomb, image):
        self.hasbomb = hasbomb
        super(MyButton, self).__init__(tk, image=image)
    def right(self,event):
        self.configure(image=self.flag)

    def left(self,event):
        # self.configure(image=self.bm)
        if self.hasbomb:
            self.configure(image=self.bm)
        else:
            self.configure(image = self.empty)


class Minesweeper:
    def __init__(self,tk,nrows,ncolumns,nbombs):
        width =10
        height = 10

        img = Image.open("qm.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.qm =  ImageTk.PhotoImage(img)

        img = Image.open("bm.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.bm =  ImageTk.PhotoImage(img)

        img = Image.open("flag.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.flag =  ImageTk.PhotoImage(img)

        img = Image.open("empty.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.empty =  ImageTk.PhotoImage(img)


        tk.title("Minesweeper")
        tk.resizable(width = True, height = True)
        style = ttk.Style()
        style.configure("TButton", font = "Serif 15", padding = 10)

        buttons = []
        for r in range(nrows):
            for c in range(ncolumns):
                button = MyButton(tk, image = self.qm, hasbomb = 0)
                # button.configure(command = button.change_picture)
                button.bind("<Button-3>", button.right)
                button.bind("<Button-1>", button.left)
                button.grid(row=r, column=c)
                button.flag = self.flag
                button.bm = self.bm
                button.empty = self.empty
                buttons.append(button)
        for i in range(nbombs):
            index = random.randint(0, nrows*ncolumns -1)
            button = buttons[index]
            button.hasbomb = 1
        self.buttons = buttons
tk = Tk()
mine = Minesweeper(tk,9,9,9)
tk.mainloop()
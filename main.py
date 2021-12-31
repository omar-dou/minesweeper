import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from matplotlib.pyplot import imshow
import numpy
import random
import os
import time

class MyButton(ttk.Button):

    def __init__(self, tk, hasbomb, image, row, column):
        self.hasbomb = hasbomb
        self.row = row
        self.column = column
        self.flagged = False
        self.clicked = False
        self.tk = tk
        super(MyButton, self).__init__(tk, image=image)

    def end(self, text):
        for rbutton in self.minesweeper.buttons:
            for button in rbutton:
                if button.hasbomb:
                    button.configure(image=self.bm)
                else:
                    if not button.clicked:
                        button.left(None)
        print(text)
        Tk.update(self)
        time.sleep(1)
        for rbutton in self.minesweeper.buttons:
            for button in rbutton:
                button.destroy()
        self.minesweeper.endgame = Label(text = text)
        self.minesweeper.timer.destroy()
        self.minesweeper.bomblab.destroy()
        self.minesweeper.endgame.grid(row=0, column=0)
        self.minesweeper.quit = ttk.Button(command = self.quit, text = "Quit")
        self.minesweeper.reset = ttk.Button(command = self.reset, text = "Play Again")
        self.minesweeper.quit.grid(row = 1, column = 3)
        self.minesweeper.reset.grid(row = 1, column = 8)

    def quit(self):
        self.tk.quit()
    def reset(self):
        self.minesweeper.endgame.destroy()
        self.minesweeper.quit.destroy()
        self.minesweeper.reset.destroy()
        self.minesweeper.create()


    def right(self,event):
        if self.clicked:
            return
        if not self.flagged:
            self.configure(image=self.flag)
            self.flagged = True
            self.minesweeper.flagleft -= 1
        else:
            self.flagged = False
            self.configure(image=self.qm)
            self.minesweeper.flagleft += 1
        self.minesweeper.bomblab.configure(text = str(self.minesweeper.flagleft))


    def left(self,event):
        # self.configure(image=self.bm)
        print("clicking", self.row, self.column)
        self.clicked = True
        if self.flagged:
            return
        if self.hasbomb:
            self.configure(image=self.bm)
            self.minesweeper.lost=True
            self.end("Game Over")
        else:
            bombs = self.bombsaround()
            if bombs ==0:
                self.configure(image = self.empty)
                for i in range(self.row-1,self.row+2):
                    if i<0 or i>= self.minesweeper.rows:
                        continue
                    for j in range(self.column-1,self.column+2):
                        if j<0 or j>= self.minesweeper.columns:
                            continue
                        if j==self.column and i==self.row:
                            continue
                        button = self.minesweeper.buttons[i][j]
                        if not button.clicked:
                            print("calling:",i,j)
                            button.left(None)
            else:
                self.configure(image = self.minesweeper.numbers[bombs-1])
            if self.minesweeper.lost is False:
                clicked = 0
                for rbutton in self.minesweeper.buttons:
                    for button in rbutton:
                        if button.clicked or button.flagged:
                            clicked += 1
                ncells=self.minesweeper.rows*self.minesweeper.columns
                if clicked == ncells - self.minesweeper.nbombs:
                    self.end("You win")

    def bombsaround(self): 
        bombs=0
        for i in range(self.row-1,self.row+2):
            if i<0 or i>= self.minesweeper.rows:
                continue
            for j in range(self.column-1,self.column+2):
                if j<0 or j>= self.minesweeper.columns:
                    continue
                if j==self.column and i==self.row:
                    continue
                # print(i,j)
                # print(self.row)
                # print(self.column)
                button = self.minesweeper.buttons[i][j]
                if button.hasbomb:
                    bombs+=1
        return bombs
       
        


class Minesweeper:
    def __init__(self,tk,nrows,ncolumns,nbombs):
        width = 10
        height = 10
        self.flagleft = nbombs
        self.rows = nrows
        self.columns = ncolumns
        self.nbombs = nbombs
        self.lost=False
        self.starttime = time.time()
        tk.geometry("{}x{}".format(nrows*38,ncolumns*38))

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

        self.numbers=[]
        for i in range(1,9):
            img = Image.open("{}.png".format(i))
            img = img.resize((width,height), Image.ANTIALIAS)
            self.numbers.append(ImageTk.PhotoImage(img))

        tk.title("Minesweeper")
        tk.resizable(width = True, height = True)
        style = ttk.Style()
        style.configure("TButton", font = "Serif 15", padding = 10)

        self.playbutton=ttk.Button(text = "Play", command = self.play)
        self.playbutton.pack()

    def play(self):
        self.playbutton.destroy()
        self.create()


    def create(self):
        self.timer = Label(text = "0")
        self.timer.grid(row = 0, column = 1, columnspan = 5)
        self.timer.after(1000, self.updatetimer)
        self.bomblab = Label(text = str(self.nbombs))
        self.bomblab.grid(row = 0, column = 9)
        buttons = []
        for r in range(self.rows):
            rbuttons = []
            for c in range(self.columns):
                button = MyButton(tk, image = self.qm, hasbomb = 0, row = r, column = c)
                # button.configure(command = button.change_picture)
                button.bind("<Button-3>", button.right)
                button.bind("<Button-1>", button.left)
                button.grid(row=r+1, column=c)
                #grid(column = 1, row = 10, columnspan = 1, rowspan = 1)
                button.flag = self.flag
                button.bm = self.bm
                button.qm = self.qm
                button.empty = self.empty
                rbuttons.append(button)
                button.minesweeper = self
            buttons.append(rbuttons)
        self.buttons = buttons
        bombcounter = 0
        while bombcounter < self.nbombs:
            rindex = random.randint(0, self.rows -1)
            cindex = random.randint(0, self.columns -1)
            rbuttons = buttons[rindex]
            button = rbuttons[cindex]
            if button.hasbomb != 1:
                button.hasbomb = 1
                bombcounter += 1
            # print(bombcounter)
            # print(cindex, rindex)                
        

        self.buttons = buttons
    def updatetimer(self):
        timestarted = int(time.time() - self.starttime)
        self.timer.configure(text = str(timestarted))
        self.timer.after(1000, self.updatetimer)
    
tk = Tk()
mine = Minesweeper(tk,15,15,2)
tk.mainloop()
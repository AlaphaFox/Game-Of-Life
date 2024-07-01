import tkinter as tk
import numpy as np
import random as rd
from tkinter import simpledialog as inputclass
from tkinter import messagebox as mb
from webbrowser import open as owp
global url
url = "https://github.com/AlaphaFox/Game-Of-Life"
def datainfo():
    rst = tk.Tk()
    rst.title("AlaphaFox生命游戏")
    A1 = tk.Label(rst,text = "AlaphaFox编写",font = 'Arial')
    A1.pack()
    A2 = tk.Label(rst,text = "基于Python 3.10.11")
    A2.pack()
    B1 = tk.Label(rst,text ="Github:")
    B1.pack()
    B2 = tk.Button(rst,text = "前往",command = lambda:owp(url))
    B2.pack()


class GameOfLife():
    def __init__(self):
        self.name = '生命游戏 - AlaphaFox Python实机'
        self.width = 500
        self.height = 450
        self.window = tk.Tk()
        self.window.title(self.name)
        self.window.geometry('{}x{}'.format(self.width, self.height))
        self.canvas = tk.Canvas(self.window, bg='white', width=self.width-100, height=self.height-50 )
        self.array = np.zeros((int((self.width-100)/20), int((self.height-50)/20)), dtype=int)
        self.start_btn=tk.Button(self.window,bg='gray',text='启动',command=self.start)
        self.pause_btn=tk.Button(self.window,bg='gray',text='暂停',command=self.pause)
        self.refresh_btn=tk.Button(self.window,bg='gray',text='重置',command=self.restart)
        self.quit_btn=tk.Button(self.window,bg='gray',text='关于',command=datainfo)
            #   设置暂停标志
        self.flag=5
            #   设置start次数，防止加速
        self.count=0
    def input_number(self):
        self.number = 20
    def pack(self):
        self.canvas.pack()
        self.start_btn.place(x=10,y=410,anchor='nw')
        self.pause_btn.place(x=150,y=410,anchor='nw')
        self.refresh_btn.place(x=290,y=410,anchor='nw')
        self.quit_btn.place(x=430, y=410, anchor='nw')

    def init_cells(self):
        count = 0
        #   随机产生细胞
        for x in range(len(self.array)):
            for y in range(len(self.array[x])):
                if count > 200:
                    return
                if rd.randint(0, 100) >= 50:
                    self.array[x][y] = 1
                    count += 1
    def draw(self):
            #   画图
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                if self.array[i][j]==1:
                    self.canvas.create_rectangle(j*20,i*20,j*20+20,i*20+20,fill='blue')
                else:
                    self.canvas.create_rectangle(j * 20, i * 20, j * 20 + 20, i * 20 + 20, fill='white')

    def start(self):
        if self.flag==1:
            return
        self.flag=1
        self.refresh()

    def pause(self):
        self.flag=0

    def refresh(self):
        if self.flag==1:
            for i in range(1, len(self.array) - 1):
                for j in range(1, len(self.array[i]) - 1):
                    sum = self.array[i][j - 1] + self.array[i - 1][j - 1] + self.array[i - 1][j] + self.array[i - 1][
                        j + 1] + self.array[i][j + 1] + self.array[i + 1][j + 1] + self.array[i + 1][j] + self.array[i + 1][ j - 1]

                        # 活细胞
                    if self.array[i][j] == 1:
                        if sum != 2 and sum != 3:
                            self.array[i][j] = 0

                    else:  # 死细胞
                        if sum == 3:
                            self.array[i][j] = 1
            self.draw()
            self.canvas.after(1000, self.refresh)
        else:
            return

    def restart(self):
        self.flag=0
        self.init_cells()
        self.start()


    def show(self):
        self.canvas.mainloop()


if __name__ == '__main__':
    mb.showinfo("Tips:","即将开始随机实机运行")
    game1 = GameOfLife()
    game1.input_number()
    game1.pack()
    game1.init_cells()
    game1.draw()
    game1.show()

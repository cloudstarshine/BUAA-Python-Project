from tkinter import *
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
import numpy as npy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import statisticMode


class StatisticLine:
    def __init__(self, master, user_name, is_admin):
        # 用户属性
        self.user_name = user_name
        self.is_admin = is_admin

        # 设置主窗口属性
        self.master = master
        self.master.title('数据统计')

        self.statistic_adjust = Frame(self.master, width=1000, height=100)
        self.statistic_adjust.pack()

        self.set_tips()

        # 添加其他部件
        self.set_line()

        # 设置子窗口
        self.statistic_line = Frame(self.master, width=1000, height=100)
        self.statistic_line.pack()

        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_name = Label(self.statistic_adjust, text='数据统计', height=2, font=word_set)
        self.label_name.place(relx=0.42, rely=0.38)

    def set_button(self):
        word_set = ("宋体", 15)

        # 返回
        self.button_exit = Button(self.statistic_line, text='返回', command=self.cmd_exit, font=word_set)
        self.button_exit.place(relx=0.7, rely=0.3, width=90, height=30)

    def set_line(self):
        self.fig = plt.figure(figsize=(10, 5), dpi=100, frameon=True)

        # 做题日志数据库
        # 创建链接
        con_journal = sqlite3.connect('./SQL/user_journal.db')

        # 创建游标对象
        cur_journal = con_journal.cursor()

        sql_journal = 'SELECT * FROM ' + self.user_name + '_journal'
        tem_list = list(cur_journal.execute(sql_journal))

        cur_journal.close()
        con_journal.close()

        question = ['Choice', 'Judgement', 'Short Answer']
        wrong_short_num = tem_list[2][3] - tem_list[2][4]
        total_num = [tem_list[0][3], tem_list[1][3], tem_list[2][4]]
        right_num = [tem_list[0][4], tem_list[1][4], tem_list[2][4] - wrong_short_num]

        plt.plot(question, right_num, color='b', label='Right Number')
        plt.plot(question, total_num, color='r', label='Total Number')

        plt.legend()
        plt.grid()
        plt.xlabel('Kind')
        plt.ylabel('Number')

        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def cmd_exit(self):
        self.statistic_adjust.destroy()
        self.statistic_line.destroy()
        self.canvas.get_tk_widget().destroy()
        statisticMode.StatisticMode(self.master, self.user_name, self.is_admin)


if __name__ == '__main__':
    root = Tk()
    StatisticLine(root, 'admin1')
    root.mainloop()

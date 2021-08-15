from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3

import maindesk
import statisticBar
import statisticForm
import statisticLine


class StatisticMode:
    def __init__(self, master, user_name, is_admin):
        # 用户相关信息
        self.user_name = user_name
        self.is_admin = is_admin

        # 设置主窗口属性
        self.master = master
        self.master.title('主程序')

        # 设置子窗口
        self.statistic_mode = Frame(self.master, width=1000, height=750)
        self.statistic_mode.pack()

        # 添加其他部件
        self.set_tips()
        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_tips = Label(self.statistic_mode, text='请选择统计图类型', height=2, font=word_set)
        self.label_tips.place(relx=0.387, rely=0.2)

    def set_button(self):
        word_set = ("宋体", 20)

        # 表格
        self.button_form = Button(self.statistic_mode, text='表格', command=self.cmd_form, font=word_set)
        self.button_form.place(relx=0.24, rely=0.43, width=140, height=80)

        # 柱形图
        self.button_bar = Button(self.statistic_mode, text='柱形图', command=self.cmd_bar, font=word_set)
        self.button_bar.place(relx=0.62, rely=0.43, width=140, height=80)

        # 折线图
        self.button_line = Button(self.statistic_mode, text='折线图', command=self.cmd_line, font=word_set)
        self.button_line.place(relx=0.24, rely=0.62, width=140, height=80)

        # 取消
        self.button_cancel = Button(self.statistic_mode, text='取消', command=self.cmd_cancel, font=word_set)
        self.button_cancel.place(relx=0.62, rely=0.62, width=140, height=80)

    def cmd_form(self):
        self.statistic_mode.destroy()
        statisticForm.StatisticForm(self.master, self.user_name, self.is_admin)

    def cmd_bar(self):
        self.statistic_mode.destroy()
        statisticBar.StatisticBar(self.master, self.user_name, self.is_admin)

    def cmd_line(self):
        self.statistic_mode.destroy()
        statisticLine.StatisticLine(self.master, self.user_name, self.is_admin)

    def cmd_cancel(self):
        self.statistic_mode.destroy()
        maindesk.MainDesk(self.master, self.user_name, self.is_admin)


if __name__ == '__main__':
    root = Tk()
    StatisticMode(root, 'admin1', True)
    root.mainloop()

from tkinter import *
from tkinter import ttk
import sqlite3

import statisticMode


class StatisticForm:
    def __init__(self, master, user_name, is_admin):
        # 用户属性
        self.user_name = user_name
        self.is_admin = is_admin

        # 设置主窗口属性
        self.master = master
        self.master.title('数据统计')

        self.statistic_adjust = Frame(self.master, width=1000, height=250)
        self.statistic_adjust.pack()

        self.set_tips()

        # 添加其他部件
        self.set_form()

        # 设置子窗口
        self.statistic_form = Frame(self.master, width=1000, height=200)
        self.statistic_form.pack()

        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_name = Label(self.statistic_adjust, text='数据统计', height=2, font=word_set)
        self.label_name.place(relx=0.42, rely=0.38)

    def set_button(self):
        word_set = ("宋体", 15)

        # 返回
        self.button_exit = Button(self.statistic_form, text='返回', command=self.cmd_exit, font=word_set)
        self.button_exit.place(relx=0.7, rely=0.3, width=90, height=30)

    def set_form(self):
        # 做题日志数据库
        # 创建链接
        con_journal = sqlite3.connect('./SQL/user_journal.db')

        # 创建游标对象
        cur_journal = con_journal.cursor()

        sql_journal = 'SELECT * FROM ' + self.user_name + '_journal'
        tem_list = list(cur_journal.execute(sql_journal))

        cur_journal.close()
        con_journal.close()

        wrong_short_num = tem_list[2][3] - tem_list[2][4]

        choice_rate = 0
        judgement_rate = 0
        short_rate = 0

        if tem_list[0][3] != 0:
            choice_rate = tem_list[0][4] / tem_list[0][3]
        if tem_list[1][3] != 0:
            judgement_rate = tem_list[1][4] / tem_list[1][3]
        if tem_list[2][3] != 0:
            short_rate = (tem_list[2][4] - wrong_short_num) / tem_list[2][4]

        choice_list = ['选择题', tem_list[0][3], tem_list[0][4], choice_rate]
        judgement_list = ['判断题', tem_list[1][3], tem_list[1][4], judgement_rate]
        short_list = ['简答题', tem_list[2][4], tem_list[2][4] - wrong_short_num, short_rate]

        columns = ['题目类型', '总数', '正确数', '正确率']
        self.table = ttk.Treeview(
            master=self.master,
            height=7,
            columns=columns,
            show='headings'
        )

        word_set = ("宋体", 20)

        self.table.heading('题目类型', text='题目类型')
        self.table.heading('总数', text='总数')
        self.table.heading('正确数', text='正确数')
        self.table.heading('正确率', text='正确率')

        self.table.column('题目类型', width=250, minwidth=250, anchor=S)
        self.table.column('总数', width=250, minwidth=250, anchor=S)
        self.table.column('正确数', width=250, minwidth=250, anchor=S)
        self.table.column('正确率', width=250, minwidth=250, anchor=S)

        space = [' ', ' ', ' ', ' ']

        self.table.insert('', END, values=space)
        self.table.insert('', END, values=choice_list)
        self.table.insert('', END, values=space)
        self.table.insert('', END, values=judgement_list)
        self.table.insert('', END, values=space)
        self.table.insert('', END, values=short_list)

        self.table.pack(pady=20)

    def cmd_exit(self):
        self.statistic_adjust.destroy()
        self.statistic_form.destroy()
        self.table.destroy()
        statisticMode.StatisticMode(self.master, self.user_name, self.is_admin)


if __name__ == '__main__':
    root = Tk()
    StatisticForm(root, 'admin1', True)
    root.mainloop()

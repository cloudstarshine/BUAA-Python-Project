import csv
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3
import maindesk
import questionChoice
import questionJudgement
import questionShort


class QuestionMode:
    def __init__(self, master, user_name, is_admin, question_kind):
        # 用户相关信息
        self.user_name = user_name
        self.is_admin = is_admin

        # 问题类型
        self.question_kind = question_kind

        # 设置主窗口属性
        self.master = master
        self.master.title('主程序')

        # 设置子窗口
        self.question_mode = Frame(self.master, width=1000, height=750)
        self.question_mode.pack()

        # 添加其他部件
        self.set_tips()
        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_tips = Label(self.question_mode, text='请选择做题方式', height=2, font=word_set)
        self.label_tips.place(relx=0.387, rely=0.2)

    def set_button(self):
        word_set = ("宋体", 20)

        # 继续做题
        self.button_continue = Button(self.question_mode, text='继续做题', command=self.cmd_continue, font=word_set)
        self.button_continue.place(relx=0.24, rely=0.43, width=140, height=80)

        # 顺序做题
        self.button_order = Button(self.question_mode, text='顺序做题', command=self.cmd_order, font=word_set)
        self.button_order.place(relx=0.62, rely=0.43, width=140, height=80)

        # 随机做题
        self.button_random = Button(self.question_mode, text='随机做题', command=self.cmd_random, font=word_set)
        self.button_random.place(relx=0.24, rely=0.62, width=140, height=80)

        # 取消
        self.button_cancel = Button(self.question_mode, text='取消', command=self.cmd_cancel, font=word_set)
        self.button_cancel.place(relx=0.62, rely=0.62, width=140, height=80)

    def cmd_continue(self):
        # 做题日志数据库
        # 创建链接
        con_journal = sqlite3.connect('./SQL/user_journal.db')

        # 创建游标对象
        cur_journal = con_journal.cursor()

        sql_journal = 'SELECT * FROM ' + self.user_name + '_journal'
        tem_list = list(cur_journal.execute(sql_journal))

        self.question_mode.destroy()

        if self.question_kind == 'choice':
            questionChoice.QuestionChoice(self.master, self.user_name, self.is_admin,
                                          'continue', tem_list[0][2], 'normal')
        elif self.question_kind == 'judgement':
            questionJudgement.QuestionJudgement(self.master, self.user_name, self.is_admin,
                                                'continue', tem_list[1][2], 'normal')
        else:
            questionShort.QuestionShort(self.master, self.user_name, self.is_admin,
                                        'continue', tem_list[2][2], 'normal')

    def cmd_order(self):
        self.question_mode.destroy()
        if self.question_kind == 'choice':
            questionChoice.QuestionChoice(self.master, self.user_name, self.is_admin, 'order', 1, 'normal')
        elif self.question_kind == 'judgement':
            questionJudgement.QuestionJudgement(self.master, self.user_name, self.is_admin, 'order', 1, 'normal')
        else:
            questionShort.QuestionShort(self.master, self.user_name, self.is_admin, 'order', 1, 'normal')

    def cmd_random(self):
        self.question_mode.destroy()
        if self.question_kind == 'choice':
            questionChoice.QuestionChoice(self.master, self.user_name, self.is_admin, 'random', 1, 'normal')
        elif self.question_kind == 'judgement':
            questionJudgement.QuestionJudgement(self.master, self.user_name, self.is_admin, 'random', 1, 'normal')
        else:
            questionShort.QuestionShort(self.master, self.user_name, self.is_admin, 'random', 1, 'normal')

    def cmd_cancel(self):
        self.question_mode.destroy()
        maindesk.MainDesk(self.master, self.user_name, self.is_admin)


if __name__ == '__main__':
    root = Tk()
    QuestionMode(root, 'user_test', True, 'judgement')
    root.mainloop()

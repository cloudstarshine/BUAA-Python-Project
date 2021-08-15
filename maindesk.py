from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3

import addAdmin
import helper
import questionChoice
import questionJudgement
import questionShort
import questionSupply
import questionMode
import statisticMode


class MainDesk:
    def __init__(self, master, user_name, is_admin):
        # 用户相关信息
        self.user_name = user_name
        self.is_admin = is_admin

        # 设置主窗口属性
        self.master = master
        self.master.title('主程序')

        # 设置子窗口
        self.main_desk = Frame(self.master, width=1000, height=750)
        self.main_desk.pack()

        # 添加其他部件
        self.set_tips()
        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_tips = Label(self.main_desk, text='请选择题目类型', height=2, font=word_set)
        self.label_tips.place(relx=0.39, rely=0.2)

    def set_button(self):
        word_set = ("楷体", 20)
        offset = 0

        # 判断是否为管理员
        if self.is_admin:
            # 设置偏移量
            offset = 0.06

            # 数据统计
            self.button_question_supply = \
                Button(self.main_desk, text='题目补充', command=self.cmd_question_supply, font=word_set)
            self.button_question_supply.place(relx=0.315, rely=0.8, width=140, height=80)

            # 退出
            self.button_add_admin = Button(self.main_desk, text='添加管理员', command=self.cmd_add_admin, font=word_set)
            self.button_add_admin.place(relx=0.545, rely=0.8, width=140, height=80)

        # 选择
        self.button_choice = Button(self.main_desk, text='选择题', command=self.cmd_choice, font=word_set)
        self.button_choice.place(relx=0.2, rely=(0.49 - offset), width=140, height=80)

        # 判断
        self.button_judgement = Button(self.main_desk, text='判断题', command=self.cmd_judgement, font=word_set)
        self.button_judgement.place(relx=0.43, rely=(0.49 - offset), width=140, height=80)

        # 简答
        self.button_short_answer = Button(self.main_desk, text='简答题', command=self.cmd_short_answer, font=word_set)
        self.button_short_answer.place(relx=0.66, rely=(0.49 - offset), width=140, height=80)

        # 错题回顾
        self.button_review = Button(self.main_desk, text='错题回顾', command=self.cmd_review, font=word_set)
        self.button_review.place(relx=0.2, rely=(0.68 - offset), width=140, height=80)

        # 数据统计
        self.button_statistic = Button(self.main_desk, text='数据统计', command=self.cmd_statistic, font=word_set)
        self.button_statistic.place(relx=0.43, rely=(0.68 - offset), width=140, height=80)

        # 退出
        self.button_exit = Button(self.main_desk, text='退出', command=self.cmd_exit, font=word_set)
        self.button_exit.place(relx=0.66, rely=(0.68 - offset), width=140, height=80)

    def cmd_choice(self):
        self.main_desk.destroy()
        questionMode.QuestionMode(self.master, self.user_name, self.is_admin, 'choice')

    def cmd_judgement(self):
        self.main_desk.destroy()
        questionMode.QuestionMode(self.master, self.user_name, self.is_admin, 'judgement')

    def cmd_short_answer(self):
        self.main_desk.destroy()
        questionMode.QuestionMode(self.master, self.user_name, self.is_admin, 'short')

    def cmd_review(self):
        # 做题日志数据库
        # 创建链接
        con_journal = sqlite3.connect('./SQL/user_journal.db')

        # 创建游标对象
        cur_journal = con_journal.cursor()

        sql_journal = 'SELECT * FROM ' + self.user_name + '''_wrong
                            WHERE question_valid=\'True\'
                            LIMIT 1'''

        tem_list = list(cur_journal.execute(sql_journal))

        cur_journal.close()
        con_journal.close()

        if len(tem_list) == 0:
            messagebox.showerror('提示', '您的错题本里还没有题目呢!')
        else:
            if tem_list[0][1] == 'choice':
                self.main_desk.destroy()
                questionChoice.QuestionChoice(self.master, self.user_name,
                                              self.is_admin, 'continue', tem_list[0][2], 'fix')
            elif tem_list[0][1] == 'judgement':
                self.main_desk.destroy()
                questionJudgement.QuestionJudgement(self.master, self.user_name,
                                                    self.is_admin, 'continue', tem_list[0][2], 'fix')
            else:
                self.main_desk.destroy()
                questionShort.QuestionShort(self.master, self.user_name, self.is_admin,
                                            'continue', tem_list[0][2], 'fix')

    def cmd_statistic(self):
        self.main_desk.destroy()
        statisticMode.StatisticMode(self.master, self.user_name, self.is_admin)

    def cmd_exit(self):
        exit()

    def cmd_question_supply(self):
        self.main_desk.destroy()
        questionSupply.QuestionSupply(self.master, self.user_name, True)

    def cmd_add_admin(self):
        self.main_desk.destroy()
        addAdmin.AddAdmin(self.master, self.user_name)


if __name__ == '__main__':
    root = Tk()
    MainDesk(root, 'admin1', True)
    root.mainloop()

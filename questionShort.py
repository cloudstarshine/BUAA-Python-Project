from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3

import helper
import maindesk


class QuestionShort:
    def __init__(self, master, user_name, is_admin, question_mode, question_num, operation_type):
        # 用户相关信息
        self.user_name = user_name
        self.is_admin = is_admin

        # 问题信息
        self.question_mode = question_mode
        self.question_num = question_num
        self.operation_type = operation_type

        # 设置主窗口属性
        self.master = master
        self.master.title('主程序')

        # 设置子窗口
        self.question_short = Frame(self.master, width=1000, height=750)
        self.question_short.pack()

        # 题目数据库
        # 判断题
        # 创建链接
        con_question = sqlite3.connect('./SQL/question_data.db')

        # 创建游标对象
        cur_question = con_question.cursor()

        sql_choice = 'SELECT * FROM question_short WHERE short_id= ' + str(question_num)

        question_database = cur_question.execute(sql_choice)
        self.question_list = list(question_database)

        # 添加其他部件
        self.set_tips()
        self.set_button()

        helper.do_right(self.user_name, 'short', self.question_num)

    def set_tips(self):
        word_set = ("宋体", 20)

        # 简答题题干
        question_text = str(self.question_num) + '. ' + self.question_list[0][1]

        # 标签
        self.label_question = Label(self.question_short, text=question_text,
                                    wraplength=760, height=5, font=word_set)
        self.label_question.place(relx=0.12, rely=0.07)

    def set_button(self):
        word_set = ("宋体", 20)

        # 显示答案
        self.button_show = Button(self.question_short, text='显示答案', command=self.cmd_show, font=word_set)
        self.button_show.place(relx=0.2, rely=0.35, width=120, height=50)

        if self.operation_type == 'fix':
            self.button_remove = Button(self.question_short, text='移出错题本', command=self.cmd_remove, font=word_set)
            self.button_remove.place(relx=0.2, rely=0.84, width=120, height=50)
        else:
            # 加入错题本
            self.button_sign = Button(self.question_short, text='加入错题本', command=self.cmd_sign, font=word_set)
            self.button_sign.place(relx=0.68, rely=0.35, width=120, height=50)

            # 上一题
            self.button_last = Button(self.question_short, text='上一题', command=self.cmd_last, font=word_set)
            self.button_last.place(relx=0.2, rely=0.84, width=120, height=50)

        # 下一题
        self.button_next = Button(self.question_short, text='下一题', command=self.cmd_next, font=word_set)
        self.button_next.place(relx=0.44, rely=0.84, width=120, height=50)

        # 退出
        self.button_cancel = Button(self.question_short, text='退出', command=self.cmd_cancel, font=word_set)
        self.button_cancel.place(relx=0.68, rely=0.84, width=120, height=50)

    def cmd_show(self):
        word_set = ("宋体", 20)

        # 选择题题干
        question_answer = str(self.question_num) + '. ' + self.question_list[0][2]

        # 标签
        label_answer = Label(self.question_short, text=question_answer,
                             wraplength=760, height=5, font=word_set)
        label_answer.place(relx=0.12, rely=0.45)

    def cmd_sign(self):
        helper.do_wrong(self.user_name, 'short', self.question_num)
        messagebox.showinfo('提示', '加入成功!')

    def cmd_last(self):
        if self.question_mode != 'random':
            if self.question_num == 1:
                messagebox.showinfo('提示', '已经是第一道题了哟!')
            else:
                self.question_short.destroy()
                QuestionShort(self.master, self.user_name, self.is_admin,
                              self.question_mode, self.question_num - 1, 'normal')
        else:
            # 创建链接
            con_question = sqlite3.connect('./SQL/question_data.db')

            # 创建游标对象
            cur_question = con_question.cursor()

            sql_count = 'SELECT COUNT(*) FROM question_short'
            total_num = list(cur_question.execute(sql_count))[0][0]

            cur_question.close()
            con_question.close()

            new_question_id = random.randint(1, total_num)
            while new_question_id == self.question_num:
                new_question_id = random.randint(1, total_num)

            self.question_short.destroy()
            QuestionShort(self.master, self.user_name, self.is_admin,
                          self.question_mode, new_question_id, 'normal')

    def cmd_next(self):
        if self.operation_type == 'fix':
            helper.fix_next(self.master, self.user_name, self.is_admin,
                            'short', self.question_num, self.question_short)
        else:
            # 创建链接
            con_question = sqlite3.connect('./SQL/question_data.db')

            # 创建游标对象
            cur_question = con_question.cursor()

            sql_count = 'SELECT COUNT(*) FROM question_short'
            total_num = list(cur_question.execute(sql_count))[0][0]

            cur_question.close()
            con_question.close()

            if self.question_mode != 'random':
                if self.question_num == total_num:
                    messagebox.showinfo('提示', '已经是最后一题了哟!')
                else:
                    self.question_short.destroy()
                    QuestionShort(self.master, self.user_name, self.is_admin,
                                  self.question_mode, self.question_num + 1, 'normal')
            else:
                new_question_id = random.randint(1, total_num)
                while new_question_id == self.question_num:
                    new_question_id = random.randint(1, total_num)

                self.question_short.destroy()
                QuestionShort(self.master, self.user_name, self.is_admin,
                              self.question_mode, new_question_id, 'normal')

    def cmd_cancel(self):
        self.question_short.destroy()
        maindesk.MainDesk(self.master, self.user_name, self.is_admin)

    def cmd_remove(self):
        helper.remove_wrong(self.user_name, 'short', self.question_num)
        messagebox.showinfo('提示', '移除成功')


if __name__ == '__main__':
    root = Tk()
    QuestionShort(root, 'user_test', False, 'continue', 1, 'fix')
    root.mainloop()

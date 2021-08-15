from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3

import helper
import maindesk


class QuestionChoice:
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
        self.master.title('选择题')

        # 设置子窗口
        self.question_choice = Frame(self.master, width=1000, height=750)
        self.question_choice.pack()

        # 题目数据库
        # 选择题
        # 创建链接
        con_question = sqlite3.connect('./SQL/question_data.db')

        # 创建游标对象
        cur_question = con_question.cursor()

        sql_choice = 'SELECT * FROM question_choice WHERE choice_id= ' + str(question_num)

        question_database = cur_question.execute(sql_choice)
        self.question_list = list(question_database)

        # 添加其他部件
        self.set_tips()
        self.set_input_box()
        self.set_button()

        cur_question.close()
        con_question.close()

    def set_tips(self):
        word_set = ("宋体", 15)

        # 选择题题干
        question_text = str(self.question_num) + '. ' + self.question_list[0][1]

        # 标签
        self.label_question = Label(self.question_choice, text=question_text,
                                    wraplength=760, height=5, font=word_set)
        self.label_question.place(relx=0.12, rely=0.07)

        # 选择题选项
        # A
        question_text = 'A: ' + self.question_list[0][2]

        # 标签
        self.label_A = Label(self.question_choice, text=question_text,
                             wraplength=760, height=5, font=word_set)
        self.label_A.place(relx=0.12, rely=0.22)

        # B
        question_text = 'B: ' + self.question_list[0][3]

        # 标签
        self.label_B = Label(self.question_choice, text=question_text,
                             wraplength=760, height=5, font=word_set)
        self.label_B.place(relx=0.12, rely=0.32)

        # C
        question_text = 'C: ' + self.question_list[0][4]

        # 标签
        self.label_C = Label(self.question_choice, text=question_text,
                             wraplength=760, height=5, font=word_set)
        self.label_C.place(relx=0.12, rely=0.42)

        # D
        question_text = 'D: ' + self.question_list[0][5]

        # 标签
        self.label_D = Label(self.question_choice, text=question_text,
                             wraplength=760, height=5, font=word_set)
        self.label_D.place(relx=0.12, rely=0.52)

        word_set = ("宋体", 20)

        # tips
        question_text = '请输入您的答案，多选题不同选项之间不需要任何字符'

        self.label_tips = Label(self.question_choice, text=question_text,
                                wraplength=760, height=5, font=word_set)
        self.label_tips.place(relx=0.12, rely=0.6)

    def set_input_box(self):
        word_set = ("times", 20)

        self.entry_answer = Entry(self.question_choice, font=word_set)
        self.entry_answer.place(relx=0.12, rely=0.72, width=300, height=50)

    def set_button(self):
        word_set = ("宋体", 20)

        # 提交
        self.button_commit = Button(self.question_choice, text='提交', command=self.cmd_commit, font=word_set)
        self.button_commit.place(relx=0.45, rely=0.72, width=120, height=50)

        if self.operation_type == 'fix':
            # 移出错题本
            self.button_remove = Button(self.question_choice, text='移出错题本', command=self.cmd_remove, font=word_set)
            self.button_remove.place(relx=0.2, rely=0.84, width=120, height=50)
        else:
            # 上一题
            self.button_last = Button(self.question_choice, text='上一题', command=self.cmd_last, font=word_set)
            self.button_last.place(relx=0.2, rely=0.84, width=120, height=50)

        # 下一题
        self.button_next = Button(self.question_choice, text='下一题', command=self.cmd_next, font=word_set)
        self.button_next.place(relx=0.44, rely=0.84, width=120, height=50)

        # 退出
        self.button_cancel = Button(self.question_choice, text='退出', command=self.cmd_cancel, font=word_set)
        self.button_cancel.place(relx=0.68, rely=0.84, width=120, height=50)

    def cmd_commit(self):
        if self.entry_answer.get() == self.question_list[0][6]:
            word_set = ("宋体", 15)

            label_result = Label(self.question_choice, text='恭喜您，回答正确!', height=5, font=word_set)
            label_result.place(relx=0.7, rely=0.72)
            helper.do_right(self.user_name, 'choice', self.question_num)
        else:
            word_set = ("宋体", 15)

            text = '回答错误，正确答案为:' + self.question_list[0][6]
            label_result = Label(self.question_choice, text=text, height=5, font=word_set)
            label_result.place(relx=0.7, rely=0.72)
            helper.do_wrong(self.user_name, 'choice', self.question_num)

    def cmd_last(self):
        if self.question_mode != 'random':
            if self.question_num == 1:
                messagebox.showinfo('提示', '已经是第一道题了哟!')
            else:
                self.question_choice.destroy()
                QuestionChoice(self.master, self.user_name, self.is_admin,
                               self.question_mode, self.question_num - 1, 'normal')
        else:
            # 创建链接
            con_question = sqlite3.connect('./SQL/question_data.db')

            # 创建游标对象
            cur_question = con_question.cursor()

            sql_count = 'SELECT COUNT(*) FROM question_choice'
            total_num = list(cur_question.execute(sql_count))[0][0]

            cur_question.close()
            con_question.close()

            new_question_id = random.randint(1, total_num)
            while new_question_id == self.question_num:
                new_question_id = random.randint(1, total_num)

            self.question_choice.destroy()
            QuestionChoice(self.master, self.user_name, self.is_admin,
                           self.question_mode, new_question_id, 'normal')

    def cmd_next(self):
        if self.operation_type == 'fix':
            helper.fix_next(self.master, self.user_name, self.is_admin,
                            'choice', self.question_num, self.question_choice)
        else:
            # 创建链接
            con_question = sqlite3.connect('./SQL/question_data.db')

            # 创建游标对象
            cur_question = con_question.cursor()

            sql_count = 'SELECT COUNT(*) FROM question_choice'
            total_num = list(cur_question.execute(sql_count))[0][0]

            cur_question.close()
            con_question.close()

            if self.question_mode != 'random':
                if self.question_num == total_num:
                    messagebox.showinfo('提示', '已经是最后一题了哟!')
                else:
                    self.question_choice.destroy()
                    QuestionChoice(self.master, self.user_name, self.is_admin,
                                   self.question_mode, self.question_num + 1, 'normal')
            else:
                new_question_id = random.randint(1, total_num)
                while new_question_id == self.question_num:
                    new_question_id = random.randint(1, total_num)

                self.question_choice.destroy()
                QuestionChoice(self.master, self.user_name, self.is_admin,
                               self.question_mode, new_question_id, 'normal')

    def cmd_cancel(self):
        self.question_choice.destroy()
        maindesk.MainDesk(self.master, self.user_name, self.is_admin)

    def cmd_remove(self):
        helper.remove_wrong(self.user_name, 'choice', self.question_num)
        messagebox.showinfo('提示', '移除成功')


if __name__ == '__main__':
    root = Tk()
    QuestionChoice(root, 'user1', False, 'continue', 1, 'normal')
    root.mainloop()

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3
import maindesk
import questionImport


class QuestionSupply:
    def __init__(self, master, user_name, is_admin):
        # 用户相关信息
        self.user_name = user_name
        self.is_admin = is_admin

        # 设置主窗口属性
        self.master = master
        self.master.title('主程序')

        # 设置子窗口
        self.question_supply = Frame(self.master, width=1000, height=750)
        self.question_supply.pack()

        # 添加其他部件
        self.set_tips()
        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_tips = Label(self.question_supply, text='请选择题目类型', height=2, font=word_set)
        self.label_tips.place(relx=0.387, rely=0.2)

    def set_button(self):
        word_set = ("宋体", 20)

        # 选择
        self.button_choice = Button(self.question_supply, text='选择题', command=self.cmd_choice, font=word_set)
        self.button_choice.place(relx=0.24, rely=0.43, width=140, height=80)

        # 判断
        self.button_judgement = Button(self.question_supply, text='判断题', command=self.cmd_judgement, font=word_set)
        self.button_judgement.place(relx=0.62, rely=0.43, width=140, height=80)

        # 简答
        self.button_short_answer \
            = Button(self.question_supply, text='简答题', command=self.cmd_short_answer, font=word_set)
        self.button_short_answer.place(relx=0.24, rely=0.62, width=140, height=80)

        # 简答
        self.button_cancel = Button(self.question_supply, text='取消', command=self.cmd_cancel, font=word_set)
        self.button_cancel.place(relx=0.62, rely=0.62, width=140, height=80)

    def cmd_choice(self):
        self.question_supply.destroy()
        questionImport.QuestionImport(self.master, self.user_name, True, 'choice')

    def cmd_judgement(self):
        self.question_supply.destroy()
        questionImport.QuestionImport(self.master, self.user_name, True, 'judgement')

    def cmd_short_answer(self):
        self.question_supply.destroy()
        questionImport.QuestionImport(self.master, self.user_name, True, 'short')

    def cmd_cancel(self):
        self.question_supply.destroy()
        maindesk.MainDesk(self.master, self.user_name, True)


if __name__ == '__main__':
    root = Tk()
    QuestionSupply(root, 'user_test', True)
    root.mainloop()

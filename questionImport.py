import csv
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3
import questionSupply


class QuestionImport:
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
        self.question_import = Frame(self.master, width=1000, height=750)
        self.question_import.pack()

        # 添加其他部件
        self.set_tips()
        self.set_input_box()
        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 30)

        if self.question_kind == 'choice':
            question_text = '请导入含有选择题的csv文件，导入格式为包含csv文件完整文件名称的相对路径/绝对路径。' \
                   'csv文件内部格式为题目,选项A,选项B,选项C,选项D,答案（A,B,C,D,多选题各选项之间不加任何符号）。'
        elif self.question_kind == 'judgement':
            question_text = '请导入含有判断题的csv文件，导入格式为包含csv文件完整文件名称的相对路径/绝对路径。' \
                   'csv文件内部格式为题目,答案（True/False）。'
        else:
            question_text = '请导入含有简答题的csv文件，导入格式为包含csv文件完整文件名称的相对路径/绝对路径。' \
                   'csv文件内部格式为题目,答案。'

        # 标签
        self.label_tips = Label(self.question_import, text=question_text,
                                wraplength=700, height=5, font=word_set)
        self.label_tips.place(relx=0.15, rely=0.2)

    def set_input_box(self):
        word_set = ("times", 20)

        self.entry_path = Entry(self.question_import, font=word_set)
        self.entry_path.place(relx=0.15, rely=0.52, width=700, height=70)

    def set_button(self):
        word_set = ("宋体", 20)

        # 数据统计
        self.button_import = Button(self.question_import, text='导入', command=self.cmd_import, font=word_set)
        self.button_import.place(relx=0.315, rely=0.7, width=140, height=60)

        # 退出
        self.button_cancel = Button(self.question_import, text='取消', command=self.cmd_cancel, font=word_set)
        self.button_cancel.place(relx=0.545, rely=0.7, width=140, height=60)

    def cmd_import(self):
        # 打开对应的csv文件
        csv_path = self.entry_path.get()

        # 判断打开文件的路径是否错误
        is_right_path = True

        try:
            csv_question = open(csv_path, 'r')
            csv_reader = csv.reader(csv_question)
        except Exception as e:
            is_right_path = False
            messagebox.showerror('格式错误', '路径格式错误或未找到文件，请重试')

        if is_right_path:
            # 创建链接
            con_question = sqlite3.connect('./SQL/question_data.db')

            # 创建游标对象
            cur_question = con_question.cursor()

            # 创建题库插入语句
            if self.question_kind == 'choice':
                sql_question_import = 'insert into question_choice(choice_content,choice_A,choice_B,' \
                                      'choice_C,choice_D,choice_answer) values(?,?,?,?,?,?)'
            elif self.question_kind == 'judgement':
                sql_question_import = 'insert into question_judgement(judgement_content,judgement_answer) values(?,?)'
            else:
                sql_question_import = 'insert into question_short(short_content,short_answer) values(?,?)'

            # 创建检查重复性语句
            sql_check = 'SELECT * FROM question_' + self.question_kind

            # 导入失败标示
            is_import_failed = False

            for question in csv_reader:
                is_new_question = True
                # 执行检查sql语句
                check_base = cur_question.execute(sql_check)

                for one in check_base:
                    if one[1] == question[0]:
                        is_new_question = False
                        break

                # 执行插入sql语句
                if is_new_question:
                    try:
                        cur_question.execute(sql_question_import, tuple(question))
                        con_question.commit()
                    except Exception as e:
                        messagebox.showerror('导入失败', '文件数据格式错误，请修复后重试')
                        is_import_failed = True
                        break
            if not is_import_failed:
                messagebox.showinfo('导入成功', '数据已成功导入题库')

            cur_question.close()
            con_question.close()
            csv_question.close()

            self.question_import.destroy()
            questionSupply.QuestionSupply(self.master, self.user_name, True)

    def cmd_cancel(self):
        self.question_import.destroy()
        questionSupply.QuestionSupply(self.master, self.user_name, True)


if __name__ == '__main__':
    root = Tk()
    QuestionImport(root, 'user_test', True, 'judgement')
    root.mainloop()

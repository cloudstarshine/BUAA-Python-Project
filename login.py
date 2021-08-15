from tkinter import *
from tkinter import messagebox
import random
import sqlite3
import register
import maindesk


def verification_creator():
    origin_verification = list('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
    outcome_verification = ''
    for i in range(4):
        outcome_verification += origin_verification[random.randint(0, len(origin_verification) - 1)]
    return outcome_verification


class Login:
    def __init__(self, master):
        # 设置主窗口属性
        self.master = master
        self.master.title('登录')

        # 设置子窗口
        self.login = Frame(self.master, width=1000, height=750)
        self.login.pack()

        # 添加其他部件
        self.set_input_box()
        self.set_button()

    def set_input_box(self):
        word_set = ("宋体", 30)

        # 标签
        self.label_tips = Label(self.login, text='欢迎使用Quick-Python训练平台',
                                height=2, font=word_set)
        self.label_tips.place(relx=0.3, rely=0.2)

        word_set = ("宋体", 20)

        self.label_name = Label(self.login, text='用户名', height=2, font=word_set)
        self.label_name.place(relx=0.3, rely=0.38)

        self.label_password = Label(self.login, text='密 码', height=2, font=word_set)
        self.label_password.place(relx=0.3, rely=0.48)

        self.label_verification = Label(self.login, text='验证码', height=2, font=word_set)
        self.label_verification.place(relx=0.3, rely=0.58)

        word_set = ("times", 20)

        # 输入框
        self.entry_name = Entry(self.login, font=word_set)
        self.entry_name.place(relx=0.42, rely=0.38, width=300, height=50)

        self.entry_password = Entry(self.login, font=word_set, show='*')
        self.entry_password.place(relx=0.42, rely=0.48, width=300, height=50)

        tip_verification = StringVar()
        tip_verification.set('点击验证码刷新，请注意区分大小写...')
        self.entry_verification = Entry(self.login, textvariable=tip_verification, font=word_set)
        self.entry_verification.place(relx=0.42, rely=0.58, width=220, height=50)

        # 验证码按钮
        word_set = ("times", 20)
        self.text_verification = verification_creator()

        self.button_verification = Button(self.login, text=self.text_verification,
                                          command=self.change_verification, font=word_set)
        self.button_verification.place(relx=0.64, rely=0.58, width=80, height=50)

    def set_button(self):
        word_set = ("宋体", 20)
        # 登录
        self.button_login = Button(self.login, text='登录', command=self.cmd_login, font=word_set)
        self.button_login.place(relx=0.3, rely=0.7, width=110, height=70)

        # 注册
        self.button_register = Button(self.login, text='注册', command=self.cmd_register, font=word_set)
        self.button_register.place(relx=0.455, rely=0.7, width=110, height=70)

        # 退出
        self.button_exit = Button(self.login, text='退出', command=self.cmd_exit, font=word_set)
        self.button_exit.place(relx=0.61, rely=0.7, width=110, height=70)

    def cmd_login(self):
        is_admin, is_user, is_right_verification = self.login_judge()
        if is_admin:
            if is_right_verification:
                messagebox.showinfo('登录成功', '欢迎您，管理员%s!' % self.entry_name.get())
                user_name = self.entry_name.get()
                self.login.destroy()
                maindesk.MainDesk(self.master, user_name, True)
            else:
                self.change_verification()
                messagebox.showerror('登录失败', '验证码错误，请检查后重试')
        elif is_user:
            if is_right_verification:
                messagebox.showinfo('登录成功', '欢迎您，%s，祝您学习愉快!' % self.entry_name.get())
                user_name = self.entry_name.get()
                self.login.destroy()
                maindesk.MainDesk(self.master, user_name, False)
            else:
                self.change_verification()
                messagebox.showerror('登录失败', '验证码错误，请检查后重试')
        else:
            self.change_verification()
            messagebox.showerror('登录失败', '用户名或密码错误，请检查后重试')

    def cmd_register(self):
        self.login.destroy()
        register.Register(self.master)

    def cmd_exit(self):
        exit()

    def change_verification(self):
        self.text_verification = verification_creator()
        self.button_verification.config(text=self.text_verification)

    def login_judge(self):
        is_admin = False
        is_user = False
        is_right_verification = False

        # 检验管理员账号
        # 创建链接
        con_login = sqlite3.connect('./SQL/user_data.db')

        # 创建游标对象
        cur_login = con_login.cursor()

        # 设置查询sql语句
        sql_select = '''SELECT * FROM user_login'''

        # 检索数据库
        user_table = cur_login.execute(sql_select)
        for i in user_table:
            if i[1] == self.entry_name.get() and i[2] == self.entry_password.get():
                if i[3] == 'True':
                    is_admin = True
                else:
                    is_user = True
                break
        cur_login.close()
        con_login.close()

        # 检查验证码
        if is_admin or is_user:
            if self.entry_verification.get() == self.text_verification:
                is_right_verification = True

        return is_admin, is_user, is_right_verification


if __name__ == '__main__':
    root = Tk()
    Login(root)
    root.mainloop()

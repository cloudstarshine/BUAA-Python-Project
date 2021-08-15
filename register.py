from tkinter import *
from tkinter import messagebox
import login
import sqlite3


class Register:
    def __init__(self, master):
        # 修正主窗口
        self.master = master
        self.master.title('注册')

        # 创建子窗口
        self.register = Frame(self.master, width=1000, height=750)
        self.register.pack()

        # 添加其他部件
        self.set_input_box()
        self.set_button()

    def set_input_box(self):
        word_set = ("宋体", 18)

        # 标签
        self.label_name = Label(self.register, text='用户名', height=2, font=word_set)
        self.label_name.place(relx=0.3, rely=0.23)

        self.label_password = Label(self.register, text='密  码', height=2, font=word_set)
        self.label_password.place(relx=0.3, rely=0.33)

        self.label_confirm = Label(self.register, text='确认密码', height=2, font=word_set)
        self.label_confirm.place(relx=0.3, rely=0.43)

        self.label_verification = Label(self.register, text='验证码', height=2, font=word_set)
        self.label_verification.place(relx=0.3, rely=0.53)

        word_set = ("times", 20)

        # 输入框
        self.entry_name = Entry(self.register, font=word_set)
        self.entry_name.place(relx=0.42, rely=0.23, width=300, height=50)

        self.entry_password = Entry(self.register, font=word_set, show='*')
        self.entry_password.place(relx=0.42, rely=0.33, width=300, height=50)

        self.entry_confirm = Entry(self.register, font=word_set, show='*')
        self.entry_confirm.place(relx=0.42, rely=0.43, width=300, height=50)

        tip_verification = StringVar()
        tip_verification.set('点击验证码刷新，请注意区分大小写...')
        self.entry_verification = Entry(self.register, textvariable=tip_verification, font=word_set)
        self.entry_verification.place(relx=0.42, rely=0.53, width=220, height=50)

        # 验证码按钮
        word_set = ("times", 20)
        self.text_verification = login.verification_creator()

        self.button_verification = Button(self.register, text=self.text_verification,
                                          command=self.change_verification, font=word_set)
        self.button_verification.place(relx=0.64, rely=0.53, width=80, height=50)

    def set_button(self):
        word_set = ("宋体", 15)
        # 注册
        self.button_login = Button(self.register, text='注册成功', command=self.cmd_register, font=word_set)
        self.button_login.place(relx=0.3, rely=0.65, width=110, height=70)

        self.button_exit = Button(self.register, text='取消', command=self.cmd_cancel, font=word_set)
        self.button_exit.place(relx=0.61, rely=0.65, width=110, height=70)

    def change_verification(self):
        self.text_verification = login.verification_creator()
        self.button_verification.config(text=self.text_verification)

    def cmd_register(self):
        is_null_name, is_exist_name, is_null_password, \
            is_equal_password, is_right_verification = self.register_judge()
        if is_null_name:
            self.change_verification()
            messagebox.showerror('注册失败', '请输入用户名')
        elif is_exist_name:
            self.change_verification()
            messagebox.showerror('注册失败', '用户名已存在，请重试')
        elif is_null_password:
            self.change_verification()
            messagebox.showerror('注册失败', '请输入密码')
        elif not is_equal_password:
            self.change_verification()
            messagebox.showerror('注册失败', '两次输入的密码不同，请重试')
        elif not is_right_verification:
            self.change_verification()
            messagebox.showerror('注册失败', '验证码错误，请重试')
        else:
            # 创建链接
            con_register = sqlite3.connect('./SQL/user_data.db')

            # 创建游标对象
            cur_register = con_register.cursor()

            # 设置查询sql语句
            sql_add = '''insert into user_login(user_name,user_password,user_is_admin) values(?,?,?)'''

            # 检索数据库
            cur_register.execute(sql_add, (self.entry_name.get(), self.entry_password.get(), 'False'))
            con_register.commit()
            cur_register.close()
            con_register.close()
            messagebox.showinfo('注册成功', '欢迎您，%s!请登录' % self.entry_name.get())
            self.register.destroy()
            login.Login(self.master)

    def cmd_cancel(self):
        self.register.destroy()
        login.Login(self.master)

    def register_judge(self):
        is_null_name = True
        is_exist_name = True
        is_null_password = True
        is_equal_password = False
        is_right_verification = False

        # 检查空用户名
        if self.entry_name.get() != '':
            is_null_name = False

        # 检查用户名重复
        if not is_null_name:
            is_exist_name = False
            # 创建链接
            con_register = sqlite3.connect('./SQL/user_data.db')

            # 创建游标对象
            cur_register = con_register.cursor()

            # 设置查询sql语句
            sql_select = '''SELECT * FROM user_login'''

            # 检索数据库
            user_table = cur_register.execute(sql_select)
            for i in user_table:
                if i[1] == self.entry_name.get():
                    is_exist_name = True
                    break
            cur_register.close()
            con_register.close()

        # 检查密码是否为空
        if not is_exist_name:
            if self.entry_password.get() != '':
                is_null_password = False

        # 检查两次密码是否相同
        if not is_null_password:
            if self.entry_password.get() == self.entry_confirm.get():
                is_equal_password = True

        # 检查验证码
        if is_equal_password:
            if self.entry_verification.get() == self.text_verification:
                is_right_verification = True

        return is_null_name, is_exist_name, is_null_password, is_equal_password, is_right_verification


if __name__ == '__main__':
    root = Tk()
    Register(root)
    root.mainloop()

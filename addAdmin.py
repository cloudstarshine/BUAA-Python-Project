from tkinter import *
from tkinter import messagebox
import sqlite3
import maindesk


class AddAdmin:
    def __init__(self, master, user_name):
        # 设置主窗口属性
        self.master = master
        self.master.title('选择管理员')

        # 设置用户属性
        self.user_name = user_name

        # 设置子窗口
        self.add_admin = Frame(self.master, width=1000, height=750)
        self.add_admin.pack()

        # 添加其他部件
        self.set_tips()
        self.set_input_box()
        self.set_button()

    def set_tips(self):
        word_set = ("宋体", 25)

        # 标签
        self.label_tips = Label(self.add_admin, text='请选择需要任命的管理员',
                                height=2, font=word_set)
        self.label_tips.place(relx=0.375, rely=0.2)

        word_set = ("宋体", 20)

        self.label_name = Label(self.add_admin, text='用户名', height=2, font=word_set)
        self.label_name.place(relx=0.3, rely=0.38)

        self.label_password = Label(self.add_admin, text='密 码', height=2, font=word_set)
        self.label_password.place(relx=0.3, rely=0.48)

    def set_input_box(self):
        word_set = ("宋体", 20)

        # 输入框
        self.entry_name = Entry(self.add_admin, font=word_set)
        self.entry_name.place(relx=0.42, rely=0.38, width=300, height=50)

        self.entry_password = Entry(self.add_admin, font=word_set, show='*')
        self.entry_password.place(relx=0.42, rely=0.48, width=300, height=50)

    def set_button(self):
        word_set = ("宋体", 20)
        # 登录
        self.button_login = Button(self.add_admin, text='确认', command=self.cmd_add, font=word_set)
        self.button_login.place(relx=0.3, rely=0.65, width=110, height=70)

        self.button_exit = Button(self.add_admin, text='取消', command=self.cmd_cancel, font=word_set)
        self.button_exit.place(relx=0.61, rely=0.65, width=110, height=70)

    def cmd_add(self):
        is_admin = False
        is_user = False

        # 检验管理员账号
        # 创建链接
        con_add = sqlite3.connect('./SQL/user_data.db')

        # 创建游标对象
        cur_add = con_add.cursor()

        # 设置查询sql语句
        sql_select = '''SELECT * FROM user_login'''

        # 检索数据库
        user_table = cur_add.execute(sql_select)
        for i in user_table:
            if i[1] == self.entry_name.get() and i[2] == self.entry_password.get():
                if i[3] == 'True':
                    is_admin = True
                else:
                    is_user = True
                break

        if is_admin:
            messagebox.showerror('提示', '%s 已是管理员!' % self.entry_name.get())
        elif is_user:
            sql_set = '''UPDATE user_login
                         SET user_is_admin=\'True\'
                         WHERE user_name=\'''' + self.entry_name.get() + '\''
            cur_add.execute(sql_set)
            con_add.commit()
            messagebox.showinfo('提示', '管理员添加成功!')
        else:
            messagebox.showerror('提示', '用户名或密码错误，请重试')

        cur_add.close()
        con_add.close()

    def cmd_cancel(self):
        self.add_admin.destroy()
        maindesk.MainDesk(self.master, self.user_name, True)


if __name__ == '__main__':
    root = Tk()
    AddAdmin(root, 'admin1')
    root.mainloop()

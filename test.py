import sqlite3


def run():
    # 创建链接
    con_login = sqlite3.connect('./SQL/user_data.db')

    # 创建游标对象
    cur_login = con_login.cursor()

    sql_select = '''SELECT * FROM user_login'''
    user_table = cur_login.execute(sql_select)
    for i in user_table:
        print(i)
    print()
    cur_login.close()
    con_login.close()

    # 创建链接
    con_question = sqlite3.connect('./SQL/question_data.db')

    # 创建游标对象
    cur_question = con_question.cursor()

    sql_select1 = 'SELECT * FROM question_choice'
    question_choice = cur_question.execute(sql_select1)
    for i in question_choice:
        print(i)
    print()

    sql_select2 = 'SELECT * FROM question_judgement'
    question_judgement = cur_question.execute(sql_select2)
    for i in question_judgement:
        print(i)
    print()

    sql_select3 = 'SELECT * FROM question_short'
    question_short = cur_question.execute(sql_select3)
    for i in question_short:
        print(i)
    print()

    cur_question.close()
    con_question.close()


def run2():
    # 做题日志数据库
    # 创建链接
    con_journal = sqlite3.connect('./SQL/user_journal.db')

    # 创建游标对象
    cur_journal = con_journal.cursor()

    sql = 'SELECT * FROM admin1_wrong'
    tem_list = cur_journal.execute(sql)
    for i in tem_list:
        print(i)


if __name__ == '__main__':
    run2()

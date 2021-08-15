import csv
import sqlite3
import helper


def run():
    # 登录数据库
    # 创建链接
    con_login = sqlite3.connect('./SQL/user_data.db')

    # 创建游标对象
    cur_login = con_login.cursor()

    # 创建登录表的sql语句
    sql_login = '''create table user_login(
                    user_id INTEGER primary key autoincrement,
                    user_name VARCHAR not null,
                    user_password VARCHAR not null,
                    user_is_admin VARCHAR not null
                    )'''

    # 执行sql语句
    try:
        cur_login.execute(sql_login)
        print('user_data create successfully')
    except Exception as e:
        print(e)
        print('user_data create failed')

    # 创建登录表插入语句
    sql_login = '''
                insert into user_login(user_name,user_password,user_is_admin) values(?,?,?);
                '''

    # 执行sql语句
    try:
        cur_login.executemany(sql_login, [('user1', '123456', 'False'),
                                          ('admin1', '123456admin', 'True')])
        con_login.commit()
        print('user_data insert successfully')
        a = cur_login.execute('SELECT * FROM user_login')
        for i in a:
            print(i)
    except Exception as e:
        print(e)
        print('user_data insert failed')
    finally:
        cur_login.close()
        con_login.close()

    # 题目数据库
    # 选择题
    # 创建链接
    con_question = sqlite3.connect('./SQL/question_data.db')

    # 创建游标对象
    cur_question = con_question.cursor()

    # 创建选择题表的sql语句
    sql_question = '''create table question_choice(
                    choice_id INTEGER primary key autoincrement,
                    choice_content VARCHAR not null,
                    choice_A VARCHAR not null,
                    choice_B VARCHAR not null,
                    choice_C VARCHAR not null,
                    choice_D VARCHAR not null,
                    choice_answer VARCHAR not null
                    )'''

    # 执行sql语句
    try:
        cur_question.execute(sql_question)
        print('question choice create successfully')
    except Exception as e:
        print(e)
        print('question choice create failed')


    # 判断题
    # 创建判断题表的sql语句
    sql_question = '''create table question_judgement(
                    judgement_id INTEGER primary key autoincrement,
                    judgement_content VARCHAR not null,
                    judgement_answer VARCHAR not null
                    )'''

    # 执行sql语句
    try:
        cur_question.execute(sql_question)
        print('question judgement create successfully')
    except Exception as e:
        print(e)
        print('question judgement create failed')


    # 判断题
    # 创建判断题表的sql语句
    sql_question = '''create table question_short(
                    short_id INTEGER primary key autoincrement,
                    short_content VARCHAR not null,
                    short_answer VARCHAR not null
                    )'''

    # 执行sql语句
    try:
        cur_question.execute(sql_question)
        print('question short create successfully')
    except Exception as e:
        print(e)
        print('question short create failed')
    finally:
        cur_question.close()
        con_question.close()

    # 做题日志数据库
    helper.create_sql('user1')
    helper.create_sql('admin1')

    cmd_import('./CSVDATA/choice.csv', 'choice')
    cmd_import('./CSVDATA/judgement.csv', 'judgement')
    cmd_import('./CSVDATA/short_answer.csv', 'short')


def cmd_import(csv_path, question_kind):
    csv_question = open(csv_path, 'r')
    csv_reader = csv.reader(csv_question)

    # 创建链接
    con_question = sqlite3.connect('./SQL/question_data.db')

    # 创建游标对象
    cur_question = con_question.cursor()

    # 创建题库插入语句
    if question_kind == 'choice':
        sql_question_import = 'insert into question_choice(choice_content,choice_A,choice_B,' \
                              'choice_C,choice_D,choice_answer) values(?,?,?,?,?,?)'
    elif question_kind == 'judgement':
        sql_question_import = 'insert into question_judgement(judgement_content,judgement_answer) values(?,?)'
    else:
        sql_question_import = 'insert into question_short(short_content,short_answer) values(?,?)'

    # 创建检查重复性语句
    sql_check = 'SELECT * FROM question_' + question_kind

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
            cur_question.execute(sql_question_import, tuple(question))
            con_question.commit()

    cur_question.close()
    con_question.close()
    csv_question.close()


if __name__ == '__main__':
    run()

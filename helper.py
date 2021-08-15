from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import sqlite3
import maindesk
import questionChoice
import questionJudgement
import questionShort


def create_sql(user_name):
    # 做题日志数据库
    # 创建链接
    con_journal = sqlite3.connect('./SQL/user_journal.db')

    # 创建游标对象
    cur_journal = con_journal.cursor()

    # 创建总体日志表的sql语句
    sql_journal = 'create table ' + user_name + '''_journal(
                    journal_id INTEGER primary key autoincrement,
                    question_type VARCHAR not null,
                    question_now INTEGER not null,
                    question_total INTEGER not null,
                    question_right INTEGER not null
                    )'''

    # 执行sql语句
    try:
        cur_journal.execute(sql_journal)
        print('user_journal create successfully')
    except Exception as e:
        print(e)
        print('user_journal create failed')

    # 创建日志插入语句
    sql_journal = 'insert into ' + user_name +\
                  '_journal(question_type,question_now,question_total,question_right) values(?,?,?,?)'

    # 执行sql语句
    try:
        cur_journal.executemany(sql_journal, [('choice', 1, 0, 0), ('judgement', 1, 0, 0), ('short', 1, 0, 0)])
        con_journal.commit()
        print('user_journal insert successfully')
    except Exception as e:
        print(e)
        print('user_journal insert failed')

    # 创建错题记录表
    sql_journal = 'create table ' + user_name + '''_wrong(
                        wrong_id INTEGER primary key autoincrement,
                        question_type VARCHAR not null,
                        question_id INTEGER not null,
                        question_times INTEGER not null,
                        question_right INTEGER not null,
                        question_valid VARCHAR not null
                        )'''
    try:
        cur_journal.execute(sql_journal)
        print('user_wrong create successfully')
    except Exception as e:
        print(e)
        print('user_wrong create failed')
    finally:
        cur_journal.close()
        con_journal.close()


def do_right(user_name, question_type, question_id):
    # 做题日志数据库
    # 创建链接
    con_journal = sqlite3.connect('./SQL/user_journal.db')

    # 创建游标对象
    cur_journal = con_journal.cursor()

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_journal'
        print(list(cur_journal.execute(sql_journal)))

    sql_journal = 'SELECT * FROM ' + user_name + '_journal WHERE question_type = \'' + question_type + '\''

    journal_list = list(cur_journal.execute(sql_journal))[0]

    sql_journal = 'UPDATE ' + user_name + '''_journal
                        SET question_now=''' + str(question_id) + ',question_total=' + str(journal_list[3] + 1) \
                  + ',question_right=' + str(journal_list[4] + 1) + '''
                        WHERE question_type=\'''' + question_type + '\''

    cur_journal.execute(sql_journal)
    con_journal.commit()

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_journal'
        print(list(cur_journal.execute(sql_journal)))

    cur_journal.close()
    con_journal.close()


def do_wrong(user_name, question_type, question_id):
    # 做题日志数据库
    # 创建链接
    con_journal = sqlite3.connect('./SQL/user_journal.db')

    # 创建游标对象
    cur_journal = con_journal.cursor()

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_journal'
        print(list(cur_journal.execute(sql_journal)))

    sql_journal = 'SELECT * FROM ' + user_name + '_journal WHERE question_type = \'' + question_type + '\''

    journal_list = list(cur_journal.execute(sql_journal))[0]

    sql_journal = 'UPDATE ' + user_name + '''_journal
                            SET question_now=''' + str(question_id) + ',question_total=' \
                  + str(journal_list[3] + 1) + '''
                            WHERE question_type=\'''' + question_type + '\''

    cur_journal.execute(sql_journal)
    con_journal.commit()

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_journal'
        print(list(cur_journal.execute(sql_journal)))

    # 加入错题集
    sql_journal = 'SELECT * FROM ' + user_name + '''_wrong 
                    WHERE question_type=\'''' + question_type + '\' AND question_id=' + str(question_id)

    tem_list = list(cur_journal.execute(sql_journal))

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_wrong'
        print(list(cur_journal.execute(sql_journal)))

    if len(tem_list) == 0:
        sql_journal = 'insert into ' + user_name + \
                      '_wrong(question_type,question_id,question_times,question_right,question_valid) values(?,?,?,?,?)'
        cur_journal.execute(sql_journal, (question_type, question_id, 1, 0, 'True'))
        con_journal.commit()

        if __name__ == '__main__':
            sql_journal = 'SELECT * FROM ' + user_name + '_wrong'
            print(list(cur_journal.execute(sql_journal)))
            print()
    else:
        if tem_list[0][5] == 'True':
            sql_journal = 'UPDATE ' + user_name + '''_wrong
                                SET question_times=''' + str(tem_list[0][3] + 1) + '''
                                WHERE question_id=''' + str(question_id)
        else:
            sql_journal = 'UPDATE ' + user_name + '''_wrong
                                            SET question_times=1, question_right=0, question_valid=\'True\'
                                            WHERE question_id=''' + str(question_id)
        cur_journal.execute(sql_journal)
        con_journal.commit()

        if __name__ == '__main__':
            sql_journal = 'SELECT * FROM ' + user_name + '_wrong'
            print(list(cur_journal.execute(sql_journal)))
            print()

    cur_journal.close()
    con_journal.close()


def remove_wrong(user_name, question_type, question_id):
    # 做题日志数据库
    # 创建链接
    con_journal = sqlite3.connect('./SQL/user_journal.db')

    # 创建游标对象
    cur_journal = con_journal.cursor()

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_wrong'
        print(list(cur_journal.execute(sql_journal)))

    sql_journal = 'SELECT * FROM ' + user_name + '''_wrong 
                    WHERE question_type=\'''' + question_type + '\' AND question_id=' + str(question_id)

    tem_list = list(cur_journal.execute(sql_journal))

    if len(tem_list) == 0:
        messagebox.showinfo('提示', '这道题已经不在错题本里了!')
    else:
        sql_journal = 'UPDATE ' + user_name + '''_wrong
                       SET question_valid=\'False\'
                       WHERE question_type=\'''' + question_type + '\' AND question_id=' + str(question_id)

        cur_journal.execute(sql_journal)
        con_journal.commit()

    if __name__ == '__main__':
        sql_journal = 'SELECT * FROM ' + user_name + '_wrong'
        print(list(cur_journal.execute(sql_journal)))

    cur_journal.close()
    con_journal.close()


def fix_next(master, user_name, is_admin, question_type, question_id, window):
    # 做题日志数据库
    # 创建链接
    con_journal = sqlite3.connect('./SQL/user_journal.db')

    # 创建游标对象
    cur_journal = con_journal.cursor()

    sql_journal = 'SELECT * FROM ' + user_name + '''_wrong
                    WHERE question_type=\'''' + question_type + '\' AND question_id=' + str(question_id)

    wrong_id = list(cur_journal.execute(sql_journal))[0][0] + 1

    sql_journal = 'SELECT COUNT(*) FROM ' + user_name + '''_wrong
                        WHERE wrong_id>=''' + str(wrong_id)

    judge = list(cur_journal.execute(sql_journal))[0][0]

    not_found = True

    while judge > 0:
        sql_journal = 'SELECT * FROM ' + user_name + '''_wrong
                            WHERE wrong_id=''' + str(wrong_id)
        tem_list = list(cur_journal.execute(sql_journal))

        if tem_list[0][5] != 'True':
            judge -= 1
            wrong_id += 1
            continue
        else:
            if tem_list[0][1] == 'choice':
                window.destroy()
                questionChoice.QuestionChoice(master, user_name, is_admin, 'continue', tem_list[0][2], 'fix')
            elif tem_list[0][1] == 'judgement':
                window.destroy()
                questionJudgement.QuestionJudgement(master, user_name, is_admin, 'continue', tem_list[0][2], 'fix')
            else:
                window.destroy()
                questionShort.QuestionShort(master, user_name, is_admin, 'continue', tem_list[0][2], 'fix')
            not_found = False
            break

    if not_found:
        messagebox.showinfo('提示', '已经是最后一题了哟!')

    cur_journal.close()
    con_journal.close()


if __name__ == '__main__':
    # create_sql('user1')
    # do_right('user1', 'choice', 1)
    # do_wrong('user1', 'judgement', 1)
    # remove_wrong('user1', 'choice', 2)
    draw_bar_number('admin1')

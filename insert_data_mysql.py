#!/usr/bin/python
#-*-coding=utf-8
# 

import sys
import MySQLdb
import time
import random
import string

def CreateTableSql(table_name):
    create_table_sql = "create table " + table_name + \
        "(time_" + RandomChar(20) + " varchar(25), "\
        "a_" + RandomChar(20) + " char(120), "\
        "b_" + RandomChar(20) + " char(120), "\
        "c_" + RandomChar(20) + " char(120), "\
        "d_" + RandomChar(20) + " char(120), "\
        "e_" + RandomChar(20) + " char(120), "\
        "f_" + RandomChar(20) + " char(120), "\
        "g_" + RandomChar(20) + " char(120), "\
        "h_" + RandomChar(20) + " char(120), "\
        "i_" + RandomChar(20) + " char(120), "\
        "j_" + RandomChar(20) + " char(120), "\
        "k_" + RandomChar(20) + " char(120), "\
        "l_" + RandomChar(20) + " char(120), "\
        "m_" + RandomChar(20) + " char(120), "\
        "n_" + RandomChar(20) + " char(120))"
    return create_table_sql


def InsertDataSql(table_name):
    insert_data_sql = "insert into " + table_name + \
        " values('" + str(time.strftime('%a %b %d %H:%M:%S %Y',time.localtime(time.time()))) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "', " +\
        "'" + RandomChar(80) + "')"
    return insert_data_sql


def RandomChar(n):
    random_char = ''.join([random.choice(string.letters+string.digits) for e in range(n)])
    return random_char


if __name__ == '__main__':

    start_time = str(time.strftime('%a %b %d %H:%M:%S %Y',time.localtime(time.time())))
    logfile = open("/home/shilong/Temp/insert_mysql_data_log.txt", "a")
    print >> logfile, "==================== %s ====================" % start_time
    try:
        conn = MySQLdb.connect(host="192.168.88.124",user="root",passwd="dingjia",db="scutech")
        cur = conn.cursor()
    except MySQLdb.DatabaseError as e:
        error, = e.args
        print >> logfile, error.message
        sys.exit(0)
    tables = ['scutech_one', 'scutech_two', 'scutech_three', 'scutech_four', 'scutech_five', 'scutech_six']
    i = 0
    for t in tables:
        j = 1
        # create_table_sql = CreateTableSql(t)
        # try:
        #     cur.execute(create_table_sql)
        #     print >> logfile, "Table %s Created!" % t.upper()
        # except MySQLdb.DatabaseError as e:
        #     error = e.args
        #     print >> logfile, "Create table %s raising some Errors:" % t.upper(), error
        #     sys.exit(0)
        while j <= 100:
            i += 1
            insert_data_sql = InsertDataSql(t)
            try:
                cur.execute(insert_data_sql)
            except MySQLdb.DatabaseError as e:
                error, = e.args
                print >> logfile, "Insert into table %s raising some Errors: " % t.upper(), error.message
                break
            if i%1000 == 0:
                conn.commit()
                time.sleep(5)
            j += 1

        print >> logfile, "Table %s has inserted %d records" % (t.upper(), j-1)
    conn.commit()

    cur.close()
    conn.close()
    print >> logfile, "All Table Insert Completed!"
    end_time = str(time.strftime('%a %b %d %H:%M:%S %Y',time.localtime(time.time())))
    print >> logfile, "==================== %s ====================\n" % end_time
    logfile.close()

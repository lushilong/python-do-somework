#!/usr/bin/python
#-*-coding=utf-8
# 

import sys
import cx_Oracle
import time
import random
import string

def CreateTableSql(table_name):
    create_table_sql = "create table " + table_name + \
        "(time_" + RandomChar(20) + " varchar2(25), "\
        "a_" + RandomChar(20) + " varchar2(150 char), "\
        "b_" + RandomChar(20) + " varchar2(150 char), "\
        "c_" + RandomChar(20) + " varchar2(150 char), "\
        "d_" + RandomChar(20) + " varchar2(150 char), "\
        "e_" + RandomChar(20) + " varchar2(150 char), "\
        "f_" + RandomChar(20) + " varchar2(150 char), "\
        "g_" + RandomChar(20) + " varchar2(150 char), "\
        "h_" + RandomChar(20) + " varchar2(150 char), "\
        "i_" + RandomChar(20) + " varchar2(150 char), "\
        "j_" + RandomChar(20) + " varchar2(150 char), "\
        "k_" + RandomChar(20) + " varchar2(150 char), "\
        "l_" + RandomChar(20) + " varchar2(150 char), "\
        "m_" + RandomChar(20) + " varchar2(150 char), "\
        "n_" + RandomChar(20) + " varchar2(150 char))"
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

    logfile = open("/home/shilong/Temp/insertdata_log.txt", "a")
    time_now = str(time.strftime('%a %b %d %H:%M:%S %Y',time.localtime(time.time())))
    print >> logfile, "==================== %s ====================" % time_now
    try:
        conn = cx_Oracle.connect("scutech/dingjia@192.168.88.124:1521/orcl")
        cur = conn.cursor()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print >> logfile, error.message
        sys.exit(0)
    tables = ['scutech_one', 'scutech_two', 'scutech_three']
    
    for i in [0, 1, 2]:
        
        create_table_sql = CreateTableSql(tables[i])
        try:
            cur.execute(create_table_sql)
            print >> logfile, "Table %s Created!" % tables[i].upper()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print >> logfile, "Create table %s raising some Errors: " % tables[i].upper(), error.message
            sys.exit(0)
        j = 1
        while j <= 1000:
            insert_data_sql = InsertDataSql(tables[i])
            try:
                cur.execute(insert_data_sql)
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                print >> logfile, "Insert into table %s raising some Errors: " % tables[i].upper(), error.message
                break
            if j%1000 == 0:
                conn.commit()
                time.sleep(1)
            j += 1

        conn.commit()
        print >> logfile, "Table %s has inserted %d records" % (tables[i].upper(), j-1)

    cur.close()
    conn.close()
    print >> logfile, "All Table Insert Completed!\n\n"
    logfile.close()

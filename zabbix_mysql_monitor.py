#!/usr/local/Python/bin/python  
# -*- coding: utf-8 -*-
from __future__ import division
import MySQLdb
import time
import sys
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

def mysql_dml(sql):    
    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='xxx',port=53306,connect_timeout=100)
        conn.select_db('information_schema')
        cur = conn.cursor()         
        count = cur.execute(sql)
        conn.commit()         
        if count == 0:
            result = 0
        else:
            result = cur.fetchall()
        return result
        cur.close()
        conn.close()
    except Exception,e:
        print "mysql dml error:" ,e

def compute_persecond(*tuple_arg):
    if len(tuple_arg)== 1:
        value_1 = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(tuple_arg[0]))[0][0]
        time.sleep(10)
        value_2 = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(tuple_arg[0]))[0][0]
        print (int(value_2)-int(value_1))/10
    elif len(tuple_arg)== 2:
        value_commit_1 = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(tuple_arg[0]))[0][0]
        value_rollback_1 = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(tuple_arg[1]))[0][0]
        time.sleep(10)
        value_commit_2 = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(tuple_arg[0]))[0][0]
        value_rollback_2 = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(tuple_arg[1]))[0][0]
        print ((int(value_commit_2)+int(value_rollback_2))-(int(value_commit_1)+int(value_rollback_1)))/10
        
def compute_buffer_usage():
    value_total = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='Innodb_buffer_pool_pages_total';")[0][0]
    value_free = mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='Innodb_buffer_pool_pages_free';")[0][0]
    print (int(value_total)-int(value_free))/int(value_total)
    
def query_only(args):
    print mysql_dml("select VARIABLE_VALUE from information_schema.GLOBAL_STATUS where VARIABLE_NAME='%s';"%(args))[0][0]
    
if sys.argv[1] == 'qps':
    compute_persecond('Queries')
elif sys.argv[1] == 'insert':
    compute_persecond('Com_insert')
elif sys.argv[1] == 'update':
    compute_persecond('Com_update')
elif sys.argv[1] == 'delete':
    compute_persecond('Com_delete')
elif sys.argv[1] == 'tps':
    compute_persecond('Com_commit','Com_rollback')
elif sys.argv[1] == 'buffer':
    compute_buffer_usage()
elif sys.argv[1] == 'buffer_requests':
    query_only('Innodb_buffer_pool_read_requests')
elif sys.argv[1] == 'buffer_requests_cannot':
    query_only('Innodb_buffer_pool_reads')
elif sys.argv[1] == 'connected':
    query_only('THREADS_CONNECTED')
elif sys.argv[1] == 'running':
    query_only('THREADS_RUNNING')
elif sys.argv[1] == 'aborted':
    query_only('ABORTED_CONNECTS')
else:
    print '请输入正确的参数:qps insert update delete tps buffer buffer_requests buffer_requests_cannot connected running aborted'

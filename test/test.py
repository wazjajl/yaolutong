#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import re

def db_select_product_url():
    set_utf8_sql = "set character_set_client='utf8';\
                set character_set_filesystem='utf8';\
                set character_set_results=utf8;\
                set character_set_connection=utf8;\
                set character_set_database=utf8;"
    s_connect = pymysql.connect(host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='yaolutong_db',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,)
    select_enterprise_contact = 'select id from company_contact where investment_enterprise=\'广东万方制药有限公司\';'
    try:
        with s_connect.cursor() as s_cursor:
            s_cursor.execute(set_utf8_sql)
            s_cursor.execute(select_enterprise_contact)
            s_result = s_cursor.fetchall()
	    if not s_result:
		print "ok"
	    else:
		print "no"
    finally:
        s_connect.close()

db_select_product_url()

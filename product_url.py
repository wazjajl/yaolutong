#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import re

# 药路通网站变量
domain = "http://www.yaolutong.com"
url_key = "http://www.yaolutong.com/so/index.aspx?page="
max_page_num = 3183
re_page_key = 'img"><a href="(.*\.html)'

#* 初始网站访问session
def request_url(page_url):
    headers = {
            'Host': 'www.yaolutong.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            }
    session = requests.Session()
    s_page = session.get(page_url, headers=headers)
    s_page.encoding = 'utf-8'
    return s_page


def db_insert_page_url(page_url):
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
    
    try:
        with s_connect.cursor() as s_cursor:
            s_cursor.execute(set_utf8_sql)
            sql = 'insert into product_page_url values(NULL, \'' + page_url + '\', \'no\')'
            s_cursor.execute(sql)
            s_connect.commit()
    finally:
        s_connect.close()

#* 获取总页数,并生成所有页面链接
def get_page_url_list(page_url):
    s = request_url(page_url)
    product_url_list = re.findall(re_page_key, s.text)
    return product_url_list

if __name__ == '__main__':
    for page in range(1, max_page_num + 1):
        page_url = url_key + str(page)
	print page_url
        product_url_list = get_page_url_list(page_url)

        for id in range(len(product_url_list)):
            product_url = domain + product_url_list[id]
    	    db_insert_page_url(product_url)
	print 'Page [' + str(page) + '] is done!'




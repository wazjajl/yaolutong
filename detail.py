#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import re

# 药路通网站变量
domain = "http://www.yaolutong.com"
start_url_count = 50024
#product_url_count = 200
product_url_count = 55000

# product_basic库
#re_product_id = 
re_product_name = '产品名称：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_approval_number = '批准文号：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_product_specifications = '产品规格：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_product_dosage = '产品剂型：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_manufacture_factory = '生产厂家：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_investment_enterprise = '招商企业：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_procuct_channels = '产品渠道：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_procuct_category = '产品类别：'.decode("utf8") + '.*bigkind=(.+?)"'
#re_procuct_category = '产品类别：'.decode("utf8") + '.*bigkind=(.+?)".*sKey=(.+?)"'
# product_detail库
re_brand_name = '商标名称：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_properties = '产品性能：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_usage = '用法用量：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_ingredients = '成    份：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_description = '产品说明：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_procuct_pack = '产品包装：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_procuct_character = '产品性状：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_investment_area = '招商区域：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
# company_contact库
re_contact_name = '<p>联系人：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_telphone = '<p>电话：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_mobilephone = '<p>手机：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_wechat = '<p>微信：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_qq = '<p>Q Q：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_mail = '<p>邮箱：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_website = '<p>网址：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_fax = '<p>传真：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_address = '<p>地址：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_postcode = '<p>邮编：'.decode("utf8") + '((?:.|\n)*?)</p>'
# 删除页面匹配
re_delete01 = '该信息已经被删除到回收站'.decode("utf8")
re_delete02 = '出错页面--药路通网'.decode("utf8")

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

#s = request_url('http://www.yaolutong.com/zhaoshang/96032.html')
#result = re.findall(re_brand_name, s.text)
#result01 = re.findall(re_product_properties, s.text)


def db_select_product_url(id):
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
    product_url_sql = 'select product_page_url,store_result from product_page_url where id=\'' + str(id) + '\';'
    try:
        with s_connect.cursor() as s_cursor:
    	    s_cursor.execute(set_utf8_sql)
	    s_cursor.execute(product_url_sql)
	    s_result = s_cursor.fetchall()
	    return (s_result[0]['store_result'], s_result[0]['product_page_url'])
    finally:
        s_connect.close()

def db_update_result(id):
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
	    s_cursor.execute(update_result_sql)
	    s_connect.commit()
    finally:
        s_connect.close()



def product_key(product_page_url):
    s = request_url(product_page_url)
    # delete msg
    delete_msg01 = re.findall(re_delete01, s.text)
    delete_msg02 = re.findall(re_delete02, s.text)
    # 判断该url是否已经被删除，或者显示404页面
    if len(delete_msg01) == 0 and len(delete_msg02)== 0:
        # product
        product_id = re.findall('(\d+)', product_page_url)
        product_name = re.findall(re_product_name, s.text)
        approval_number = re.findall(re_approval_number, s.text)
        product_specifications = re.findall(re_product_specifications, s.text)
        product_dosage = re.findall(re_product_dosage, s.text)
        manufacture_factory = re.findall(re_manufacture_factory, s.text)
        investment_enterprise = re.findall(re_investment_enterprise, s.text)
        procuct_channels = re.findall(re_procuct_channels, s.text)
        procuct_channels = re.findall(re_procuct_channels, s.text)
        procuct_category = re.findall(re_procuct_category, s.text)
        product_properties = re.findall(re_product_properties, s.text)
        product_usage = re.findall(re_product_usage, s.text)
        product_ingredients = re.findall(re_product_usage, s.text)
        product_description = re.findall(re_product_description, s.text)
        procuct_pack = re.findall(re_procuct_pack, s.text)
        procuct_character = re.findall(re_procuct_character, s.text)
        investment_area = re.findall(re_investment_area, s.text)
        # contact
        contact_name = re.findall(re_contact_name, s.text)
        telphone = re.findall(re_telphone, s.text)
        mobilephone = re.findall(re_mobilephone, s.text)
        wechat = re.findall(re_wechat, s.text)
        qq = re.findall(re_qq, s.text)
        mail = re.findall(re_mail, s.text)
        website = re.findall(re_website, s.text)
        fax = re.findall(re_fax, s.text)
        address = re.findall(re_address, s.text)
        postcode = re.findall(re_postcode, s.text)

        old_product_key_list = (product_id, product_name, approval_number, product_specifications, product_dosage, manufacture_factory, \
        investment_enterprise, procuct_channels, procuct_channels, procuct_category, product_properties, \
        product_usage, product_ingredients, product_description, procuct_pack, procuct_character, \
        investment_area, contact_name, telphone, mobilephone, wechat, qq, mail, website, fax, address, postcode) 
	# 将匹配到的unicode字符串编码为utf8
        new_product_key_list = [key[0].encode('utf8') for key in old_product_key_list]
        return new_product_key_list
    else:
	return "no"


def db_insert_product(result, product_key_list):
    # 数据库连接
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
    # 数据库字段赋值
    (product_id, product_name, approval_number, product_specifications, product_dosage, manufacture_factory, \
    investment_enterprise, procuct_channels, procuct_channels, procuct_category, product_properties, \
    product_usage, product_ingredients, product_description, procuct_pack, procuct_character, \
    investment_area, contact_name, telphone, mobilephone, wechat, qq, mail, website, fax, address, postcode) = product_key_list
    # 更新产品是否入库的结果
    update_result_sql = 'update product_page_url set store_result="yes" where id=\'' + str(id) + '\';'
    # 查询是否已经存在相应企业联系方式
    select_enterprise_contact_sql = 'select id from company_contact where investment_enterprise=\'' + investment_enterprise + '\';'
    # 设置字符集
    set_utf8_sql = "set character_set_client='utf8';\
                set character_set_filesystem='utf8';\
                set character_set_results=utf8;\
                set character_set_connection=utf8;\
                set character_set_database=utf8; \
		set character_set_server=utf8;"
    # 产品基础信息sql语句拼接
    sql_basic = 'insert into product_basic values( NULL,\
		\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'\
                .format(product_id,\
                product_name,\
                approval_number,\
                product_specifications,\
                product_dosage,\
                manufacture_factory,\
                investment_enterprise,\
                procuct_channels, \
		procuct_category)
    # 产品详情信息sql语句拼接
    sql_detail = 'insert into product_detail values( NULL,\
		\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'\
                .format(product_id,\
                product_name,\
                product_properties,\
                product_usage,\
                product_ingredients,\
                product_description,\
                procuct_pack,\
                procuct_character, \
		investment_area)
    # 产品基础信息sql语句拼接
    sql_contact = 'insert into company_contact values( NULL,\
		\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'\
                .format(investment_enterprise,\
                contact_name,\
                telphone,\
                mobilephone,\
                wechat,\
                qq,\
                mail,\
                website,\
                fax, \
		address, \
		postcode)
    try:
        with s_connect.cursor() as s_cursor:
	    if result == 'no':
	        s_cursor.execute(set_utf8_sql)
	        s_cursor.execute(sql_basic)
	        s_cursor.execute(sql_detail)
		# 判断是否已经存在该企业
		s_cursor.execute(select_enterprise_contact_sql)
		s_contact_result = s_cursor.fetchall()
		if not s_contact_result:
	            s_cursor.execute(sql_contact)
		# 更新相应url的插入结果
		s_cursor.execute(update_result_sql)
	        s_connect.commit()
	    else:
		pass
    finally:
        s_connect.close()


if __name__ == '__main__':
    for id in range(start_url_count, product_url_count + 1):
	result, product_url = db_select_product_url(id)
	product_key_list = product_key(product_url)
	if product_key_list != 'no':
	   logfile = open('product_intodb.log', 'a')
	   logfile.write(product_url + '\n')
	   db_insert_product(result, product_key_list)
	   logfile.write('Product ' + str(id) + ' is done.' + '\n')
	   logfile.close()
	else:
	    continue



